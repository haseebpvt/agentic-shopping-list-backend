from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    title: str
    description: str


class SuggestedProduct(BaseModel):
    name: str
    reason_for_suggestion: str
    note: str | None
    obvious_choice: bool


class SuggestedProductList(BaseModel):
    products: List[SuggestedProduct]


class State(BaseModel):
    image_base64: str
    product_items: List[Product]
    queries: List[str]
    preference_vector_search_results: List[str]
    suggested_products: SuggestedProductList
