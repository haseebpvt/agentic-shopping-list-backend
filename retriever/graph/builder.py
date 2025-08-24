from langgraph.graph import StateGraph, START, END

from retriever.graph.nodes import (
    orchestrator,
    search_vector_db_node,
    spawn_workers,
)
from retriever.graph.type import State


def build_graph():
    builder = StateGraph(State)

    builder.add_node("orchestrator", orchestrator)
    builder.add_node("vector_search", search_vector_db_node)

    builder.add_edge(START, "orchestrator")
    builder.add_conditional_edges("orchestrator", spawn_workers, ["vector_search"])
    builder.add_edge("vector_search", END)

    return builder.compile()


if __name__ == '__main__':
    graph = build_graph()
    result = graph.invoke({"queries": ["hello", "hey"]})
    print(result)
