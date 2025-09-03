from langchain_core.runnables import RunnableConfig
from pytidb import Table

from db.model.preference_table import PreferenceTable
from db.model.shopping_list_table import ShoppingListTable
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


def save_preference_node(state: State, config: RunnableConfig):
    # If there is no data, don't continue
    if not state.preference.preference:
        return

    table: Table = config.get("configurable", {}).get("preference_table")

    preferences_table_data = map(
        lambda text: PreferenceTable(
            user_id=state.user_id,
            text=text,
        ),
        state.preference.preference,
    )

    table.bulk_insert(list(preferences_table_data))


def save_shopping_list_node(state: State, config: RunnableConfig):
    # If there is no data, don't continue
    if not state.shopping_list.shopping_list:
        return

    table: Table = config.get("configurable", {}).get("shopping_list_table")

    shopping_list_table_data = map(
        lambda item: ShoppingListTable(
            user_id=state.user_id,
            item_name=item.item_name,
            quantity=item.quantity,
            note=item.note,
        ),
        state.shopping_list.shopping_list,
    )

    table.bulk_insert(list(shopping_list_table_data))
