import json
from elasticsearch_dsl import Search

async def get_key_by_args(*args, **kwargs) -> str:
    return f'{args}:{json.dumps({"kwargs": kwargs}, sort_keys=True)}'

def paginate_es_query(
        query: Search,
        page_size: int,
        page_number: int,
) -> Search:
    start = (page_number - 1) * page_size
    return query[start: start + page_size]
