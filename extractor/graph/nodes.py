from extractor.graph.type import State, ShoppingAndPreferenceExtraction
from llm.llm import get_llm
from prompt.prompt_loader import get_prompt_template


def extract_shopping_and_preference_node(state: State):
    llm = get_llm()

    data = {"user_text": state.user_text}
    prompt = get_prompt_template("extract_shopping_items_and_preferences", **data)

    explanation = llm.invoke(input=prompt)
    structured_putput = llm.with_structured_output(ShoppingAndPreferenceExtraction).invoke(explanation.content)

    return {"shopping_list": structured_putput.shopping_list, "preference": structured_putput.preference}
