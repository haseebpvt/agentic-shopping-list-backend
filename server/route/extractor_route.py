from typing import Annotated

from fastapi import Form, Depends, APIRouter
from pytidb import Table

from di.dependencies import get_preference_table, get_shopping_list_table
from extractor.graph.builder import build_graph as build_extractor_graph
from server.model.api_response import ApiResponse

router = APIRouter()


@router.post("/insert_data", response_model=ApiResponse)
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
