import operator
from typing import List, Annotated, TypedDict


class State(TypedDict):
    queries: List[str]
    user_id: str
    results: Annotated[list, operator.add]


class WorkerState(TypedDict):
    query: str
    user_id: str
    results: Annotated[list, operator.add]
