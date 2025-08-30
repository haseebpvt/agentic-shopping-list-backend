from langchain_core.messages import SystemMessage, HumanMessage

from graph.type import State, SuggestedProduct, SuggestedProductList, ProductList
from llm.llm import get_llm
from prompt.prompt_loader import get_prompt_template


def product_suggestion_node(state: State) -> SuggestedProduct:
    llm = get_llm()

    filtered_preferences = set(state.preference_vector_search_results)

    product_str = map(lambda p: str(p), state.product_items)

    data = {
        "products": list(product_str),
        "preferences": list(filtered_preferences),
    }

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

    return output


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
    pass


def vector_search_node(state: State):
    pass
