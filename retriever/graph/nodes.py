from langchain_core.runnables import RunnableConfig
from langgraph.types import Send

from db.vector_db_search import search_vector_db
from retriever.graph.type import State, WorkerState


def orchestrator(state: State):
    """Return a list of queries"""
    return {"queries": state["queries"]}


def search_vector_db_node(worker_state: WorkerState, config: RunnableConfig):
    """Search vector db with given query"""
    table = config.get("configurable", {}).get("shopping_list")

    results = search_vector_db(
        query=worker_state["query"],
        user_id=worker_state["user_id"],
        k=5,
        table=table
    )
    return {"results": results}


def spawn_workers(state: State):
    return [Send("vector_search", {"query": q, "user_id": state["user_id"]}) for q in state["queries"]]
