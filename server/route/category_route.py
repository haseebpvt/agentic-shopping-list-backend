from typing import Annotated

from fastapi import APIRouter, Depends

from db.database_service import DatabaseService
from di.dependencies import get_database_service

router = APIRouter()

@router.get("/categories")
async def get_categories(
        database_service: Annotated[DatabaseService, Depends(get_database_service)]
):
    categories = database_service.get_categories()

    return categories