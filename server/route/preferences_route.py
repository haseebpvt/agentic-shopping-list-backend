from typing import Annotated

from fastapi import Form, Depends, APIRouter
from pytidb import Table

from db.database_service import DatabaseService
from di.dependencies import get_preference_table, get_database_service
from server.model.api_response import ApiResponse

router = APIRouter()


@router.get("/get_preference_list")
async def get_preference_list(
        preference_table: Annotated[Table, Depends(get_preference_table)],
        user_id: str = Form(...),
        semantic_search_text: str | None = Form(None),
):
    if semantic_search_text:
        result = (
            preference_table.search(semantic_search_text)
            .filter({"user_id": user_id})
            .limit(10)
            .to_list()
        )
    else:
        result = preference_table.query(filters={"user_id": user_id}).to_list()

    # These keys should be removed from the dictionary as they are not required in the final output
    remove_keys_arr = ["text_vec", "_distance", "_score"]
    final_result = list(map(lambda item: {k: v for k, v in item.items() if k not in remove_keys_arr}, result))

    return ApiResponse(
        success=True,
        data=final_result
    )


@router.post("/update")
async def update_preference(
        database_service: Annotated[DatabaseService, Depends(get_database_service)],
        item_id: int = Form(...),
        text: str = Form(...),
):
    database_service.update_preference(item_id=item_id, text=text)

    return ApiResponse(
        success=True,
    )
