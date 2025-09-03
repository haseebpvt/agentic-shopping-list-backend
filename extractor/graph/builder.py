from langgraph.graph import StateGraph, START, END

from extractor.graph.nodes import extract_shopping_and_preference_node, save_preference_node, save_shopping_list_node
from extractor.graph.type import State


def build_graph():
    graph = StateGraph(State)

    graph.add_node("extract_shopping_and_preference_node", extract_shopping_and_preference_node)
    graph.add_node("save_preference_node", save_preference_node)
    graph.add_node("save_shopping_list_node", save_shopping_list_node)

    graph.add_edge(START, "extract_shopping_and_preference_node")
    graph.add_edge("extract_shopping_and_preference_node", "save_preference_node")
    graph.add_edge("extract_shopping_and_preference_node", "save_shopping_list_node")
    graph.add_edge("save_preference_node", END)
    graph.add_node("save_shopping_list_node", END)

    return graph.compile()
