from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    title: str
    description: str


class State(BaseModel):
    image_base64: str
    product_items: List[Product]
    queries: List[str]
    preference_vector_search_results: List[str]



