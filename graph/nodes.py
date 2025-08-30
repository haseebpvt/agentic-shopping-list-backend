from langchain_core.messages import SystemMessage, HumanMessage

from graph.type import State, SuggestedProduct, SuggestedProductList
from llm.llm import get_llm
from prompt.prompt_loader import get_prompt_template


def choose_product_node(state: State) -> SuggestedProduct:
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
