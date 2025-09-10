from pytidb.schema import TableModel, Field, FullTextField


class CategoryTable(TableModel):
    __tablename__ = "category"

    id: int | None = Field(default=None, primary_key=True)
    name: str = FullTextField()
