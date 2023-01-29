from functools import lru_cache

from core.config import settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import Search
from fastapi import Depends
from models.filters import PaginationFilter, QueryFilter
from models.person import Person
from services.utils import paginate_es_query, catch_es_not_found
from services.base import BaseService


class PersonService(BaseService):
    def __init__(self, elastic: AsyncElasticsearch):
        super().__init__(elastic)
        self.single_item_model = Person
        self.index_name = settings.service_index_map['person']


    @catch_es_not_found
    async def get_many_with_query_filter_sort_pagination(
            self,
            query: QueryFilter = Depends(),
            filter=None,
            sort=None,
            pagination: PaginationFilter = Depends(),
    ) -> list[Person] | None:
        s = Search()
        es_query = s
        if query.query:
            es_query = es_query.query(
                "multi_match",
                query=query.query,
                fields=[
                    'full_name',
                ]
            )
        query_body = paginate_es_query(
            query=es_query,
            page_size=pagination.page_size,
            page_number=pagination.page_number
        ).to_dict()
        search = await self.elastic.search(
            index=settings.person_index_name,
            body=query_body,
        )
        items = [Person(**hit['_source']) for hit in search['hits']['hits']]
        return items


@lru_cache()
def get_person_service(
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(elastic)
