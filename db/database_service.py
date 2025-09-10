from pytidb import Session
from pytidb import TiDBClient
from pytidb.sql import select, update

from db.model.category import CategoryTable
from db.model.preference_table import PreferenceTable
from db.model.shopping_list_table import ShoppingListTable


# noinspection PyTypeChecker
class DatabaseService:
    def __init__(self, client: TiDBClient):
        self.client = client

    def get_shopping_list(self, user_id: str):
        query = (
            select(ShoppingListTable, CategoryTable)
            .join(CategoryTable, CategoryTable.id == ShoppingListTable.category_id)
            .where(user_id == user_id)
        )

        with Session(self.client.db_engine) as session:
            result = session.exec(query).all()

        return result

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

    def _exec_query(self, query):
        with Session(self.client.db_engine) as session:
            session.exec(query)
            session.commit()
