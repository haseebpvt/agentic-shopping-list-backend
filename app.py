import json
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Form, Depends
from pytidb import Table

from db.database_service import DatabaseService
from di.dependencies import get_preference_table, get_shopping_list_table, get_database_service
from extractor.graph.builder import build_graph as build_extractor_graph
from server.model.api_response import ApiResponse
from server.route.product_recommendation_route import router as product_recommendation_route
from server.route.preferences_route import router as preference_route

app = FastAPI()

app.include_router(product_recommendation_route, prefix="/recommend", tags=["Recommend"])
app.include_router(preference_route, prefix="/preference", tags=["Preference"])


@app.get("/")
def read_root():
    return {"Hello": "World x"}


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


@app.get("/get_shopping_list")
async def get_shopping_list(
        database_service: Annotated[DatabaseService, Depends(get_database_service)],
        user_id: str = Form(...),
):
    result = database_service.get_shopping_list(user_id=user_id)

    final_data = list(map(lambda item: _process_result(item), result))

    return ApiResponse(
        success=True,
        data=final_data
    )


def _process_result(data):
    shopping_list, category = data
    shopping_list_json = json.loads(shopping_list.model_dump_json())
    category_json = {"category_name": category.name}

    return shopping_list_json | category_json


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info")
