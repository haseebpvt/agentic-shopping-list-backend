from pytidb.embeddings import EmbeddingFunction
from pytidb.schema import TableModel, Field, FullTextField


class PreferenceTable(TableModel):
    __tablename__ = "preference_table"
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field()
    text: str = FullTextField()
    text_vec: list[float] = EmbeddingFunction(
        "openai/text-embedding-3-small"
    ).VectorField(source_field="text")
