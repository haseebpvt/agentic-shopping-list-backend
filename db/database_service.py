from pytidb import TiDBClient
from pytidb.sql import select
from pytidb import Session

from db.model.category import CategoryTable
from db.model.shopping_list_table import ShoppingListTable


class DatabaseService:
    def __init__(self, client: TiDBClient):
        self.client = client

    def get_shopping_list(self, user_id: str):
        # noinspection PyTypeChecker
        query = (
            select(ShoppingListTable, CategoryTable)
            .join(CategoryTable, CategoryTable.id == ShoppingListTable.category_id)
            .where(user_id == user_id)
        )

        with Session(self.client.db_engine) as session:
            result = session.exec(query).all()

        return result
