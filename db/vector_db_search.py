def search_vector_db(query: str, k: int = 5):
    """
    Search and return k number of result form vector database.
    :param query: The query text
    :param k: Number of result to return
    :return: List of string representing matching data
    """
    return [f"Test query {i}" for i in range(1, 10)]
