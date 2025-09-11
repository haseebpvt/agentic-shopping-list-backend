import base64
import json
from typing import Annotated
from uuid import uuid4

from fastapi import UploadFile, File, Form, Depends, APIRouter
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from starlette.responses import StreamingResponse

from db.model.category import CategoryTable
from db.model.preference_table import PreferenceTable
from db.model.shopping_list_table import ShoppingListTable
from di.dependencies import get_preference_table, get_checkpoint_saver, get_shopping_list_table, get_category_table
from graph.builder import build_graph
from graph.type import StreamMessage, Quiz, SuggestedProductList
from server.model.api_response import ApiResponse
from server.model.quiz_resume_request import QuizResumeRequest

router = APIRouter()


@router.post("/get_product_recommendation")
async def get_product_recommendation(
        preference_table: Annotated[PreferenceTable, Depends(get_preference_table)],
        shopping_list_table: Annotated[ShoppingListTable, Depends(get_shopping_list_table)],
        category_table: Annotated[CategoryTable, Depends(get_category_table)],
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
            image_base64=str(image_base64),
            user_id=user_id,
            thread_id=thread_id,
            checkpointer=checkpointer,
            preference_table=preference_table,
            shopping_list_table=shopping_list_table,
            category_table=category_table,
        ),
        media_type="application/json",
    )


@router.post("/quiz_resume", response_model=ApiResponse[SuggestedProductList])
async def quiz_resume(
        preference_table: Annotated[PreferenceTable, Depends(get_preference_table)],
        shopping_list_table: Annotated[ShoppingListTable, Depends(get_shopping_list_table)],
        category_table: Annotated[CategoryTable, Depends(get_category_table)],
        checkpointer: Annotated[InMemorySaver, Depends(get_checkpoint_saver)],
        body: QuizResumeRequest,
):
    graph = build_graph(checkpointer=checkpointer)

    result = await graph.ainvoke(
        Command(resume={"quiz_results": body.question_and_answers}),
        config=_get_config(
            thread_id=body.thread_id,
            preference_table=preference_table,
            shopping_list_table=shopping_list_table,
            category_table=category_table,
        )
    )

    return ApiResponse[SuggestedProductList](
        success=True,
        data=result["suggested_products"],
    )


async def _workflow_stream_generator(
        preference_table: PreferenceTable,
        shopping_list_table: ShoppingListTable,
        category_table: CategoryTable,
        image_base64: str,
        user_id: str,
        thread_id: str,
        checkpointer: InMemorySaver,
):
    graph = build_graph(checkpointer=checkpointer)

    stream = graph.astream(
        input={"image_base64": image_base64, "user_id": user_id},
        config=_get_config(
            thread_id=thread_id,
            preference_table=preference_table,
            shopping_list_table=shopping_list_table,
            category_table=category_table,
        ),
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


def _get_config(
        preference_table: PreferenceTable,
        shopping_list_table: ShoppingListTable,
        category_table: CategoryTable,
        thread_id: str
):
    return {
        "configurable": {
            "thread_id": thread_id,
            "preference_table": preference_table,
            "shopping_list_table": shopping_list_table,
            "category": category_table,
        }
    }
