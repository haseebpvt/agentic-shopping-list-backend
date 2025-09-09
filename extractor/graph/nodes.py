from langchain_core.runnables import RunnableConfig
from langgraph.types import Send
from pytidb import Table

from db.model.preference_table import PreferenceTable
from db.model.shopping_list_table import ShoppingListTable
from extractor.graph.type import State, ShoppingAndPreferenceExtraction, IsDuplicatePrompt, PreferenceSearchWorkerState
from llm.llm import get_llm
from prompt.prompt_loader import get_prompt_template


def extract_shopping_and_preference_node(state: State):
    llm = get_llm()

    data = {"user_text": state.user_text}
    prompt = get_prompt_template("extract_shopping_items_and_preferences", **data)

    explanation = llm.invoke(input=prompt)
    structured_putput = llm.with_structured_output(ShoppingAndPreferenceExtraction).invoke(explanation.content)

    return {"shopping_list": structured_putput.shopping_list, "preference": structured_putput.preference}


def search_preference_node(state: PreferenceSearchWorkerState, config: RunnableConfig):
    table: Table[PreferenceTable] = config.get("configurable", {}).get("preference_table")

    result = (table.search(state.preference)
              .filter({"user_id": state.user_id})
              .limit(3)
              .to_pydantic())

    return {"vector_search_result": [item.text for item in result]}


def check_if_the_preference_already_exist(state: PreferenceSearchWorkerState):
    llm = get_llm()

    data = {"prompt": state.preference, "result": state.vector_search_result}
    prompt = get_prompt_template("duplicate_preference_check", **data)

    explanation = llm.invoke(prompt)
    structured_output = llm.with_structured_output(IsDuplicatePrompt).invoke(explanation.content)

    return {"is_duplicate": structured_output.is_duplicate}


def preference_adding_route(state: PreferenceSearchWorkerState):
    # If duplicate preference we don't have to add the preference to database
    return state.is_duplicate


def insert_preference_worker_spawn(state: State):
    return [
        Send(
            "preference_insertion",
            {"user_id": state.user_id, "preference": preference}
        ) for preference in state.preference.preference
    ]


def save_preference_node(state: PreferenceSearchWorkerState, config: RunnableConfig):
    # If there is no data, don't continue
    if not state.preference:
        return

    table: Table = config.get("configurable", {}).get("preference_table")

    preferences_table_data = map(
        lambda text: PreferenceTable(
            user_id=state.user_id,
            text=text,
        ),
        state.preference,
    )

    result = table.bulk_insert(list(preferences_table_data))

    return {}


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

    result = table.bulk_insert(list(shopping_list_table_data))

    return {}
