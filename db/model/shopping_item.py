from pytidb.embeddings import EmbeddingFunction
from pytidb.schema import TableModel, Field, FullTextField


class ShoppingItem(TableModel):
    __tablename__ = "user_preference"
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field()
    text: str = FullTextField()
    text_vec: list[float] = EmbeddingFunction(
        "openai/text-embedding-3-small"
    ).VectorField(source_field="text")
