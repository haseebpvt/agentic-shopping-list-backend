from pytidb import Table


def search_vector_db(
        query: str,
        table: Table,
        user_id: int,
        k: int = 5,
):
    """
    Search and return k number of result form vector database.
    :param user_id:
    :param table: TiDB table reference
    :param query: The query text
    :param k: Number of result to return
    :return: List of string representing matching data
    """

    df = (
        table.search(query)
        .filter({"user_id": user_id})
        .limit(k)
        .to_list()
    )

    return [item["text"] for item in df]
