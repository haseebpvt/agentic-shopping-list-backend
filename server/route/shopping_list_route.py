import json
from typing import Annotated

from fastapi import Form, Depends, APIRouter

from db.database_service import DatabaseService
from di.dependencies import get_database_service
from server.model.api_response import ApiResponse

router = APIRouter()


@router.get("/get_shopping_list")
async def get_shopping_list(
        database_service: Annotated[DatabaseService, Depends(get_database_service)],
        user_id: str = Form(...),
):
    result = database_service.get_shopping_list(user_id=user_id)

    final_data = list(map(lambda item: _process_shopping_list_result(item), result))

    return ApiResponse(
        success=True,
        data=final_data
    )


@router.post("/mark_purchased")
async def mark_purchased(
        database_service: Annotated[DatabaseService, Depends(get_database_service)],
        item_id: int = Form(...),
        is_purchased: bool = Form(...),
):
    database_service.mark_product_purchased(item_id=item_id, is_purchased=is_purchased)

    return ApiResponse(
        success=True,
    )


def _process_shopping_list_result(data):
    shopping_list, category = data
    shopping_list_json = json.loads(shopping_list.model_dump_json())
    category_json = {"category_name": category.name}

    return shopping_list_json | category_json
