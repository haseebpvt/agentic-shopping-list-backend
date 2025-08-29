import operator
from typing import List, Annotated
from pydantic import BaseModel


class State(BaseModel):
    queries: List[str]
    user_id: str
    results: Annotated[list, operator.add]


class WorkerState(BaseModel):
    query: str
    user_id: str
    results: Annotated[list, operator.add]
