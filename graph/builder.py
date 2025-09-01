from langgraph.graph import StateGraph, START, END

from di.dependencies import get_tidb_connection, get_shopping_table
from graph.nodes import (
    describe_image_node,
    generate_prompts_node,
    vector_search_node,
    product_suggestion_node, check_if_enough_preferences_available
)
from graph.type import State
from util.test_image import data


def build_graph():
    builder = StateGraph(State)

    builder.add_node("describe_image_node", describe_image_node)
    builder.add_node("generate_prompts_node", generate_prompts_node)
    builder.add_node("vector_search_node", vector_search_node)
    builder.add_node("product_suggestion_node", product_suggestion_node)

    builder.add_edge(START, "describe_image_node")
    builder.add_edge("describe_image_node", "generate_prompts_node")
    builder.add_edge("generate_prompts_node", "vector_search_node")
    builder.add_conditional_edges(
        "vector_search_node",
        check_if_enough_preferences_available,
        {
            True: "product_suggestion_node",
            False: END,
        }
    )
    builder.add_edge("product_suggestion_node", END)

    return builder.compile()


if __name__ == '__main__':
    graph = build_graph()

    conn = get_tidb_connection()
    table = get_shopping_table(tidb_client=conn)

    result = graph.invoke(
        input={"image_base64": data, "user_id": "4"},
        config={"configurable": {"preference_table": table}}
    )

    print(result)