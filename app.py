import base64
from typing import Annotated
from uuid import uuid4

import uvicorn
import json
from fastapi import FastAPI, UploadFile, File, Form, Depends
from pytidb import Table
from starlette.responses import StreamingResponse

from di.dependencies import get_shopping_table
from graph.builder import build_graph
from graph.type import StreamMessage, Quiz

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World x"}


@app.post("/get_product_recommendation")
async def get_product_recommendation(
        table: Annotated[Table, Depends(get_shopping_table)],
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
        ),
        media_type="application/json",
    )


async def _workflow_stream_generator(
        table: Table,
        image_base64: str,
        user_id: str,
        thread_id: str,
):
    graph = build_graph()

    stream = graph.astream(
        input={"image_base64": image_base64, "user_id": user_id},
        config={
            "configurable": {
                "preference_table": table,
                "thread_id": thread_id,
            }
        },
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
                        quiz=Quiz(quiz=data["quiz"])
                    )

                    yield message.model_dump_json()

                continue
        if event[0] == "custom":
            message = event[1]["message"]
            yield message


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info")
