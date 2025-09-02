from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    title: str
    description: str

    def pretty(self):
        return f"Product name: {self.title}, Product description: {self.description}"


class ProductList(BaseModel):
    products: List[Product]


class SuggestedProduct(BaseModel):
    name: str
    reason_for_suggestion: str
    note: str | None
    obvious_choice: bool


class SuggestedProductList(BaseModel):
    products: List[SuggestedProduct]


class PromptList(BaseModel):
    prompts: List[str]

class EnoughPreferences(BaseModel):
    is_enough_preferences: bool

class State(BaseModel):
    image_base64: str = ""
    user_id: str = ""
    product_items: ProductList | None = None
    queries: List[str] = []
    preference_vector_search_results: List[str] = []
    is_preferences_enough: bool = False
    suggested_products: SuggestedProductList | None = None
