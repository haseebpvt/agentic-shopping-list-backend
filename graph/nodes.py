from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from graph.type import State, SuggestedProductList, ProductList, PromptList, EnoughPreferences
from llm.llm import get_llm
from prompt.prompt_loader import get_prompt_template
from retriever.graph.builder import build_graph


def product_suggestion_node(state: State):
    llm = get_llm()

    data = _get_preference_and_product_data(state)

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


def describe_image_node(state: State):
    """Node for describing the products in the base64 image"""
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

    return {"product_items": product_list}


def generate_prompts_node(state: State):
    """Node for generating list of prompts for vector search"""
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
    vector_search_graph = build_graph()

    result = vector_search_graph.invoke(
        input={"queries": state.queries, "user_id": state.user_id},
        config=config,
    )

    return {"preference_vector_search_results": result["results"]}


def analyse_if_enough_preferences_available(state: State):
    llm = get_llm()

    data = _get_preference_and_product_data(state)
    prompt = get_prompt_template(name="check_if_enough_preferences", **data)

    explanation = llm.invoke(input=prompt)
    output = llm.with_structured_output(EnoughPreferences).invoke(explanation.content)

    return {"is_preferences_enough": output.is_enough_preferences}


def product_suggestion_or_quiz_router(state: State):
    if state.is_preferences_enough:
        return "enough"
    else:
        return "not_enough"


def _get_preference_and_product_data(state: State):
    filtered_preferences = set(state.preference_vector_search_results)

    product_str = map(lambda p: str(p), state.product_items)

    data = {
        "products": list(product_str),
        "preferences": list(filtered_preferences),
    }

    return data
