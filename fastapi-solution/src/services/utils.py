from http import HTTPStatus

from fastapi import HTTPException
from elasticsearch_dsl import Search
from elasticsearch import NotFoundError


def paginate_es_query(
        query: Search,
        page_size: int,
        page_number: int,
) -> Search:
    start = (page_number - 1) * page_size
    return query[start: start + page_size]


def catch_es_not_found(f):
    async def wrapper(*arg, **kwargs):
        try:
            await f(*arg, **kwargs)
        except NotFoundError as e:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f"Index not found. If you're testing, you should create or restore indexes first. {e}",
            )
    return wrapper
