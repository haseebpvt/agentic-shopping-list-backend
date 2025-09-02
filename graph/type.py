from pydantic import BaseModel, Field
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
    reason: str = Field(description="The reason of weather the preference is enough or not enough.")
    is_enough_preferences: bool


class QuestionAnswer(BaseModel):
    question: str
    answers: List[str]


class Quiz(BaseModel):
    quiz: List[QuestionAnswer]


class State(BaseModel):
    image_base64: str = ""
    user_id: str = ""
    product_items: ProductList | None = None
    queries: List[str] = []
    preference_vector_search_results: List[str] = []
    is_preferences_enough: EnoughPreferences | None = None
    quiz: Quiz | None = None
    suggested_products: SuggestedProductList | None = None
