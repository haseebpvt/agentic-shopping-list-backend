from pytidb.embeddings import EmbeddingFunction
from pytidb.schema import TableModel, Field, FullTextField


class ShoppingListTable(TableModel):
    __tablename__ = "shopping_list"
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field()
    item_name: str = FullTextField()
    quantity: str = FullTextField()
    note: str = FullTextField()
