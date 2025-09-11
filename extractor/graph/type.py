import operator
from typing import List, Optional, Annotated

from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str

    def __str__(self):
        return f"{self.name}: {self.id}"

class ShoppingItem(BaseModel):
    item_name: str
    quantity: str
    category_id: int
    note: str


class ShoppingList(BaseModel):
    shopping_list: List[ShoppingItem]


class UserPreference(BaseModel):
    preference: List[str]


class ShoppingAndPreferenceExtraction(BaseModel):
    shopping_list: ShoppingList
    preference: UserPreference

class IsDuplicatePrompt(BaseModel):
    is_duplicate: bool


class PreferenceSearchWorkerState(BaseModel):
    user_id: Optional[str] = None
    preference: Optional[str] = None
    vector_search_result: List[str] = []
    is_duplicate: bool = False
    inserted_preferences: Annotated[List[str], operator.add] = []


class State(BaseModel):
    user_id: str
    user_text: str = ""
    category_list: List[Category] = []
    shopping_list: ShoppingList | None = None
    preference: UserPreference | None = None
    inserted_preferences: Annotated[List[str], operator.add] = []
    inserted_shopping_list: List[str] = []
    extract_only_preferences: bool = False
