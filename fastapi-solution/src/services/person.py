from functools import lru_cache

from elasticsearch import AsyncElasticsearch

from core.config import settings
from db.elastic import ESearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from fastapi import Depends
from models.filters import PaginationFilter, QueryFilter
from models.person import Person
from services.utils import paginate_es_query
from services.base import BaseService


es = ESearch()


class PersonService(BaseService):
    def __init__(self, elastic: AsyncElasticsearch):
        super().__init__(elastic)
        self.single_item_model = Person
        self.index_name = settings.service_index_map['person']


    async def get_many_with_query_filter_sort_pagination(
            self,
            query: QueryFilter = Depends(),
            filter=None,
            sort=None,
            pagination: PaginationFilter = Depends(),
    ) -> list[Person] | None:
        es_query = Search()
        if query.query:
            es_query = es_query.query(
                MultiMatch(
                    query=query.query,
                    fields=['full_name'],
                    fuzziness=settings.search_fuzziness
                )
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
        elastic: ESearch = Depends(es.get_elastic)
) -> PersonService:
    return PersonService(elastic)  # type: ignore
