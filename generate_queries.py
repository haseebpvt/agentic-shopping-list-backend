from typing import List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from model.product import Product

load_dotenv()


class ProductQueryList(BaseModel):
    query: List[str]


def generate_queries(product: Product):
    model = ChatOpenAI()

    # Generate different queries

    # Structure the queries

    # Vector search the queries

    model.invoke(product.model_dump())
