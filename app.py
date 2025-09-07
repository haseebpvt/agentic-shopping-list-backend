import base64
import json
from typing import Annotated
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, Depends
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from pytidb import Table
from starlette.responses import StreamingResponse

from di.dependencies import get_preference_table, get_checkpoint_saver, get_shopping_list_table
from extractor.graph.builder import build_graph as build_extractor_graph
from graph.builder import build_graph
from graph.type import StreamMessage, Quiz, SuggestedProductList
from model.api_response import ApiResponse
from model.quiz_resume_request import QuizResumeRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World x"}


@app.post("/get_product_recommendation")
async def get_product_recommendation(
        table: Annotated[Table, Depends(get_preference_table)],
        checkpointer: Annotated[InMemorySaver, Depends(get_checkpoint_saver)],
        file: UploadFile = File(...),
        user_id: str = Form(...),
):
    thread_id = str(uuid4())

    # Convert image to base64
    image_file_bytes = await file.read()
    image_base64 = base64.b64encode(image_file_bytes).decode("utf-8")

    return StreamingResponse(
        _workflow_stream_generator(
            table=table,
            image_base64=str(image_base64),
            user_id=user_id,
            thread_id=thread_id,
            checkpointer=checkpointer,
        ),
        media_type="application/json",
    )


@app.post("/quiz_resume", response_model=ApiResponse[SuggestedProductList])
async def quiz_resume(
        table: Annotated[Table, Depends(get_preference_table)],
        checkpointer: Annotated[InMemorySaver, Depends(get_checkpoint_saver)],
        body: QuizResumeRequest,
):
    graph = build_graph(checkpointer=checkpointer)

    result = await graph.ainvoke(
        Command(resume={"quiz_results": body.question_and_answers}),
        config=_get_config(table=table, thread_id=body.thread_id)
    )

    return ApiResponse[SuggestedProductList](
        success=True,
        data=result["suggested_products"],
    )


@app.post("/insert_data", response_model=ApiResponse)
async def insert_shopping_list_and_preferences(
        preference_table: Annotated[Table, Depends(get_preference_table)],
        shopping_list_table: Annotated[Table, Depends(get_shopping_list_table)],
        user_id: str = Form(...),
        user_text: str = Form(...),
):
    graph = build_extractor_graph()

    config = {
        "configurable": {
            "preference_table": preference_table,
            "shopping_list_table": shopping_list_table
        }
    }

    result = await graph.ainvoke(
        input={"user_id": user_id, "user_text": user_text},
        config=config,
    )

    return ApiResponse(
        success=True
    )


# TODO: Update the endpoint
@app.get("/get-shopping-list")
async def get_shopping_list(
        shopping_list_table: Annotated[Table, Depends(get_shopping_list_table)],
        user_id: str = Form(...),
):
    result = shopping_list_table.query(filters={"user_id": user_id}).to_pydantic()

    return ApiResponse(
        success=True,
        data=result
    )


async def _workflow_stream_generator(
        table: Table,
        image_base64: str,
        user_id: str,
        thread_id: str,
        checkpointer: InMemorySaver,
):
    graph = build_graph(checkpointer=checkpointer)

    stream = graph.astream(
        input={"image_base64": image_base64, "user_id": user_id},
        config=_get_config(table=table, thread_id=thread_id),
        stream_mode=["custom", "updates"],
    )

    async for event in stream:
        print(event)

        if event[0] == "updates":
            # Check if we hit the quiz interrupt
            if "__interrupt__" in event[1]:
                data = json.loads(event[1]["__interrupt__"][0].value)

                if "quiz" in data:
                    message = StreamMessage(
                        type="quiz_interrupt",
                        message="Interrupted for getting more preferences from user.",
                        quiz=Quiz(quiz=data["quiz"]),
                        thread_id=thread_id,
                    )

                    yield message.model_dump_json()

                continue

            if "product_suggestion_node" in event[1]:
                suggested_product_list = event[1]["product_suggestion_node"]["suggested_products"]
                yield suggested_product_list.model_dump_json()
        if event[0] == "custom":
            message = event[1]
            yield json.dumps(message | {"thread_id": thread_id})


def _get_config(table: Table, thread_id: str):
    return {
        "configurable": {
            "preference_table": table,
            "thread_id": thread_id,
        }
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info")
