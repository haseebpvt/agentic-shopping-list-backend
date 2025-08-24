from langgraph.types import Send

from retriever.graph.type import State, WorkerState
from db.vector_db_search import search_vector_db


def orchestrator(state: State):
    """Return a list of queries"""
    return {"queries": state["queries"]}


def search_vector_db_node(worker_state: WorkerState):
    """Search vector db with given query"""
    results = search_vector_db(query=worker_state["query"])
    return {"results": results}


def spawn_workers(state: State):
    return [Send("vector_search", {"query": q}) for q in state["queries"]]
