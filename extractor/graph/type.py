import operator
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.sql.annotation import Annotated


class ShoppingItem(BaseModel):
    item_name: str
    quantity: str
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
    preference: str


class State(BaseModel):
    user_id: str
    user_text: str = ""
    shopping_list: ShoppingList | None = None
    preference: UserPreference | None = None
