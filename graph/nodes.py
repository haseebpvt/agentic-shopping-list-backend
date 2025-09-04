from typing import List

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.config import get_stream_writer
from langgraph.types import interrupt

from graph.type import State, SuggestedProductList, ProductList, PromptList, EnoughPreferences, Quiz, StreamMessage
from llm.llm import get_llm
from prompt.prompt_loader import get_prompt_template
from retriever.graph.builder import build_graph


def describe_image_node(state: State):
    """Node for describing the products in the base64 image"""
    _stream_message(StreamMessage(type="describe_image_node", message="Analysing Image.."))

    llm = get_llm()

    prompt = get_prompt_template("describe_image")

    result = llm.invoke(
        input=[
            HumanMessage(content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{state.image_base64}"},
                }
            ]),
        ]
    )

    product_list = llm.with_structured_output(schema=ProductList).invoke(input=result.content)

    _stream_message(StreamMessage(
        type="describe_image_node",
        message=f"Identified {len(product_list.products)} products")
    )

    return {"product_items": product_list}


def has_product_router(state: State):
    if state.product_items.products:
        return "continue"
    else:
        return "end"


def generate_prompts_node(state: State):
    """Node for generating list of prompts for vector search"""
    _stream_message(StreamMessage(type="generate_prompts_node", message="Preparing to search preferences.."))

    products = list(map(lambda p: p.pretty(), state.product_items.products))

    data = {
        "products": products
    }

    prompt = get_prompt_template("query_generation", **data)

    llm = get_llm()

    result = llm.invoke(
        input=[
            HumanMessage(content=prompt),
        ]
    )

    prompt_list = llm.with_structured_output(schema=PromptList).invoke(input=result.content)

    return {"queries": prompt_list.prompts}


def vector_search_node(state: State, config: RunnableConfig):
    """Node for vector searching user preferences"""
    _stream_message(StreamMessage(type="vector_search_node", message="Searching preferences.."))

    vector_search_graph = build_graph()

    result = vector_search_graph.invoke(
        input={"queries": state.queries, "user_id": state.user_id},
        config=config,
    )

    return {"preference_vector_search_results": result["results"]}


def analyse_if_enough_preferences_available(state: State):
    """Node for analysing if enough preferences are available"""
    _stream_message(StreamMessage(type="analyse_preferences", message="Analysing preferences.."))

    llm = get_llm()

    data = _get_product_data(state.product_items) | _get_preferences_data(state.preference_vector_search_results)
    prompt = get_prompt_template(name="check_if_enough_preferences", **data)

    explanation = llm.invoke(input=prompt)
    output = llm.with_structured_output(EnoughPreferences).invoke(explanation.content)

    return {"is_preferences_enough": output}


def product_suggestion_or_quiz_router(state: State):
    if state.is_preferences_enough.is_enough_preferences:
        return "enough"
    else:
        return "not_enough"


def quiz_generation_node(state: State):
    _stream_message(
        StreamMessage(
            type="quiz_generation_node",
            message="Hmm.. looks like I need more insights from you.."
        )
    )

    llm = get_llm()

    # Creates dictionary of data to be passed to prompt
    data = _get_product_data(state.product_items) | _get_analysis_data(state.is_preferences_enough)
    prompt = get_prompt_template("quiz_generation", **data)

    explanation = llm.invoke(prompt)
    structured_output = llm.with_structured_output(Quiz).invoke(explanation.content)

    return {"quiz": structured_output}


def user_interrupt_quiz_node(state: State):
    # HITL for getting users preferences
    response = interrupt(state.quiz.model_dump_json())

    return {"quiz_preferences": response["quiz_results"]}


def product_suggestion_node(state: State):
    _stream_message(
        StreamMessage(
            type="product_suggestion_node",
            message="Picking the best products for you.."
        )
    )

    llm = get_llm()

    data = (_get_product_data(state.product_items) |
            _get_preferences_data(state.preference_vector_search_results) |
            _get_quiz_preferences(state.quiz_preferences))

    prompt = get_prompt_template("choose_product", **data)

    result = llm.invoke(
        input=[
            HumanMessage(content=prompt),
        ]
    )

    llm_with_structured_output = llm.with_structured_output(schema=SuggestedProductList)

    output = llm_with_structured_output.invoke(
        input=[
            SystemMessage(content="Extract the content from below message"),
            HumanMessage(content=result.content)
        ]
    )

    return {"suggested_products": output}


def _get_product_data(product_list: ProductList):
    products = list(map(lambda p: p.pretty(), product_list.products))

    return {
        "products": products
    }


def _get_preferences_data(preferences_list: list[str]):
    """Returns list of unique preferences"""
    return {
        "preferences": list(set(preferences_list))
    }


def _get_analysis_data(enough_preferences: EnoughPreferences):
    """Returns the reason for why or why not the preferences are enough"""
    return {
        "analysis": enough_preferences.reason
    }


def _get_quiz_preferences(preferences: List[str]):
    """Returns the quiz preference list"""
    return {
        "quiz_preferences": preferences
    }


def _stream_message(message: StreamMessage):
    writer = get_stream_writer()
    writer(message.model_dump())
