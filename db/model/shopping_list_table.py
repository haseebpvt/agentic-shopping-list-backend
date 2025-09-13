from pytidb.embeddings import EmbeddingFunction
from pytidb.schema import TableModel, Field, FullTextField


class ShoppingListTable(TableModel):
    __tablename__ = "shopping_list_table"
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field()
    item_name: str = FullTextField()
    quantity: str = FullTextField()
    unit: str = FullTextField()
    timestamp: int = Field()
    category_id: int = Field()
    note: str = FullTextField()
    is_purchased: bool = Field(default=False)
    is_ai_suggestion: bool = Field(default=False)
