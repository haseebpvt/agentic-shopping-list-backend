import operator
from typing import List, Annotated, TypedDict


class State(TypedDict):
    queries: List[str]
    results: Annotated[list, operator.add]


class WorkerState(TypedDict):
    query: str
    results: Annotated[list, operator.add]
