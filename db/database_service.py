import time
from typing import List

from pytidb import Session, Table
from pytidb import TiDBClient
from pytidb.sql import select, update, delete

from db.model.category import CategoryTable
from db.model.preference_table import PreferenceTable
from db.model.shopping_list_table import ShoppingListTable
from extractor.graph.type import ShoppingItem


# noinspection PyTypeChecker
class DatabaseService:
    def __init__(self, client: TiDBClient, shopping_list_table: Table):
        self.client = client
        self.shopping_list_table = shopping_list_table

    def get_shopping_list(self, user_id: str):
        query = (
            select(ShoppingListTable, CategoryTable)
            .join(CategoryTable, CategoryTable.id == ShoppingListTable.category_id)
            .where(user_id == user_id)
        )

        with Session(self.client.db_engine) as session:
            result = session.exec(query).all()

        return result

    def save_to_shopping_list(
            self,
            user_id: str,
            shopping_list: List[ShoppingItem],
    ):
        shopping_list_table_data = list(
            map(
                lambda item: ShoppingListTable(
                    user_id=user_id,
                    item_name=item.item_name,
                    quantity=item.quantity,
                    unit="",
                    timestamp=time.time(),
                    category_id=item.category_id,
                    note=item.note,
                ),
                shopping_list,
            )
        )

        return self.shopping_list_table.bulk_insert(shopping_list_table_data)

    def mark_product_purchased(self, item_id: int, is_purchased: bool):
        query = (
            update(ShoppingListTable)
            .where(ShoppingListTable.id == item_id)
            .values(is_purchased=is_purchased)
        )

        self._exec_query(query)

    def update_preference(self, item_id: int, text: str):
        query = (
            update(PreferenceTable)
            .where(PreferenceTable.id == item_id)
            .values(text=text)
        )

        self._exec_query(query)

    def delete_preference(self, item_id: int):
        query = (
            delete(PreferenceTable)
            .where(PreferenceTable.id == item_id)
        )

        self._exec_query(query)

    def _exec_query(self, query):
        with Session(self.client.db_engine) as session:
            session.exec(query)
            session.commit()

    def does_product_duplicate_exists(self, user_id: str, product_name: str):
        """Checks if unpurchased product with same name exist already"""
        query = (
            select(ShoppingListTable)
            .where(
                ShoppingListTable.user_id == user_id,
                ShoppingListTable.item_name == product_name,
                ShoppingListTable.is_purchased == 0,
            )
        )

        with Session(self.client.db_engine) as session:
            result = session.exec(query).all()

        return len(result) > 0
