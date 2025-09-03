from typing import List

from pydantic import BaseModel


class ShoppingItem(BaseModel):
    user_id: str
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


class State(BaseModel):
    user_text: str = ""
    shopping_list: ShoppingList | None = None
    preference: UserPreference | None = None
