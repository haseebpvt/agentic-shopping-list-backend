from langgraph.graph import StateGraph, START, END

from graph.nodes import (
    describe_image_node,
    generate_prompts_node,
    vector_search_node,
    product_suggestion_node
)
from graph.type import State


def build_graph():
    builder = StateGraph(State)

    builder.add_node("describe_image_node", describe_image_node)
    builder.add_node("generate_prompts_node", generate_prompts_node)
    builder.add_node("vector_search_node", vector_search_node)
    builder.add_node("product_suggestion_node", product_suggestion_node)

    builder.add_edge(START, "describe_image_node")
    # Other edges
    builder.add_edge(END, "product_suggestion_node")

    return builder.compile()