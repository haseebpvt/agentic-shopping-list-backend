from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    title: str
    description: str


class ProductList(BaseModel):
    products: List[Product]
