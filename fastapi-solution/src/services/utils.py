from elasticsearch_dsl import Search


def paginate_es_query(
        query: Search,
        page_size: int,
        page_number: int,
) -> Search:
    start = (page_number - 1) * page_size
    return query[start: start + page_size]
