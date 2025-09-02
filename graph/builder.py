from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END

from di.dependencies import get_tidb_connection, get_shopping_table
from graph.nodes import (
    describe_image_node,
    generate_prompts_node,
    vector_search_node,
    product_suggestion_node,
    analyse_if_enough_preferences_available,
    product_suggestion_or_quiz_router,
    quiz_generation_node,
    user_interrupt_quiz_node,
    has_product_router
)
from graph.type import State
from util.test_image_2 import data


def build_graph():
    builder = StateGraph(State)

    builder.add_node("describe_image_node", describe_image_node)
    builder.add_node("generate_prompts_node", generate_prompts_node)
    builder.add_node("vector_search_node", vector_search_node)
    builder.add_node("analyse_preferences", analyse_if_enough_preferences_available)
    builder.add_node("quiz_generation_node", quiz_generation_node)
    builder.add_node("user_interrupt_quiz_node", user_interrupt_quiz_node)
    builder.add_node("product_suggestion_node", product_suggestion_node)

    builder.add_edge(START, "describe_image_node")
    builder.add_conditional_edges(
        "describe_image_node",
        has_product_router,
        {
            "continue": "generate_prompts_node",
            "end": END
        }
    )
    builder.add_edge("generate_prompts_node", "vector_search_node")
    builder.add_edge("vector_search_node", "analyse_preferences")
    builder.add_conditional_edges(
        "analyse_preferences",
        product_suggestion_or_quiz_router,
        {
            "enough": "product_suggestion_node",
            "not_enough": "quiz_generation_node",
        }
    )
    builder.add_edge("quiz_generation_node", "user_interrupt_quiz_node")
    builder.add_edge("product_suggestion_node", END)

    checkpointer = InMemorySaver()

    return builder.compile(checkpointer=checkpointer)


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    graph = build_graph()

    conn = get_tidb_connection()
    table = get_shopping_table(tidb_client=conn)

    stream = graph.stream(
        input={"image_base64": data, "user_id": "4"},
        config={"configurable": {"preference_table": table}}
    )

    for item in stream:
        print(item)