from typing import Annotated, List

from fastapi import APIRouter, Depends, Form
from pydantic import BaseModel

from db.database_service import DatabaseService
from di.dependencies import get_database_service
from llm.llm import get_llm
from prompt.prompt_loader import get_prompt_template
from server.model.api_response import ApiResponse

router = APIRouter()


class Category(BaseModel):
    id: int
    name: str


class CategoryList(BaseModel):
    categories: List[Category]


@router.get("/categories")
async def get_categories(
        database_service: Annotated[DatabaseService, Depends(get_database_service)]
):
    categories = database_service.get_categories()

    return categories


@router.get("/identify")
async def identify_category(
        database_service: Annotated[DatabaseService, Depends(get_database_service)],
        item_name: str = Form(...),
):
    # Get category list from db
    categories = database_service.get_categories()

    # Generate prompt
    formatted_category_list = list(map(lambda i: f"{i.name} - ID: {i.id}", categories))
    prompt = get_prompt_template(
        "identify_category",
        **{"categories": formatted_category_list, "item_name": item_name},
    )

    llm = get_llm(model_size="nano")
    result = llm.with_structured_output(CategoryList).invoke(prompt)

    return ApiResponse(
        success=True,
        data=result,
    )
