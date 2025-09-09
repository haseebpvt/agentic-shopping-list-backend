import time

from langchain_core.runnables import RunnableConfig
from langgraph.types import Send
from pytidb import Table

from db.model.category import CategoryTable
from db.model.preference_table import PreferenceTable
from db.model.shopping_list_table import ShoppingListTable
from extractor.graph.type import State, ShoppingAndPreferenceExtraction, IsDuplicatePrompt, PreferenceSearchWorkerState, \
    Category
from llm.llm import get_llm
from prompt.prompt_loader import get_prompt_template


def load_category_node(_: State, config: RunnableConfig):
    table: Table[CategoryTable] = config.get("configurable", {}).get("category")
    result = table.query().to_pydantic()

    return {
        "category_list": list(map(lambda item: Category(id=int(item.id), name=item.name), result))
    }


def extract_shopping_and_preference_node(state: State):
    llm = get_llm()

    data = {
        "user_text": state.user_text,
        "categories": list(map(lambda category: str(category), state.category_list))
    }
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

    data = {"query": state.preference, "result": state.vector_search_result}
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
        return {}

    table: Table = config.get("configurable", {}).get("preference_table")

    preferences_table_data = PreferenceTable(
        user_id=state.user_id,
        text=state.preference,
    )

    result = table.bulk_insert([preferences_table_data])

    return {"inserted_preferences": [item.text for item in result]}


def save_shopping_list_node(state: State, config: RunnableConfig):
    # If there is no data, don't continue
    if not state.shopping_list.shopping_list:
        return {}

    table: Table = config.get("configurable", {}).get("shopping_list_table")

    shopping_list_table_data = list(
        map(
            lambda item: ShoppingListTable(
                user_id=state.user_id,
                item_name=item.item_name,
                quantity=item.quantity,
                unit="",
                timestamp=time.time(),
                category_id=item.category_id,
                note=item.note,
            ),
            state.shopping_list.shopping_list,
        )
    )

    result = table.bulk_insert(shopping_list_table_data)

    return {
        "inserted_shopping_list": list(map(lambda item: item.item_name, result))
    }


def finalize_node(state: State):
    return {}
