from langgraph.graph import StateGraph, START, END

from extractor.graph.nodes import (
    extract_shopping_and_preference_node,
    save_preference_node,
    search_preference_node,
    check_if_the_preference_already_exist,
    preference_adding_route,
    insert_preference_worker_spawn,
)
from extractor.graph.type import State, PreferenceSearchWorkerState


def build_graph():
    graph = StateGraph(State)

    graph.add_node("extract_shopping_and_preference_node", extract_shopping_and_preference_node)
    graph.add_node("preference_insertion", _build_preference_inserter_graph)

    graph.add_edge(START, "extract_shopping_and_preference_node")
    graph.add_conditional_edges(
        "extract_shopping_and_preference_node",
        insert_preference_worker_spawn,
        ["preference_insertion"]
    )
    graph.add_edge("preference_insertion", END)

    return graph.compile()


def _build_preference_inserter_graph():
    graph = StateGraph(PreferenceSearchWorkerState)

    graph.add_node("search_preference_node", search_preference_node)
    graph.add_node("check_if_the_preference_already_exist", check_if_the_preference_already_exist)
    graph.add_node("save_preference_node", save_preference_node)

    graph.add_edge(START, "search_preference_node")
    graph.add_edge("search_preference_node", "check_if_the_preference_already_exist")
    graph.add_conditional_edges(
        "check_if_the_preference_already_exist",
        preference_adding_route,
        {
            True: END,
            False: "save_preference_node"
        },
    )
    graph.add_edge("save_preference_node", END)
