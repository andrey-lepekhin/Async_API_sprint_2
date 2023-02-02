from functools import lru_cache

from core.config import settings
from db.elastic import get_async_search
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.filters import PaginationFilter, QueryFilter
from models.person import Person
from services.base import BaseService


class PersonService(BaseService):
    def __init__(self, elastic: AsyncElasticsearch):
        super().__init__(elastic)
        self.single_item_model = Person
        self.index_name = settings.service_index_map['person']

    async def get_by_id(self, id: str) -> Person | None:
        item = await self.async_search_db.get_by_id(
            self.index_name, id
        )
        if item:
            return self.single_item_model(**item)
        return None

    async def get_many_with_query_filter_sort_pagination(
            self,
            query: QueryFilter = Depends(),
            index_filter=None,
            sort=None,
            pagination: PaginationFilter = Depends(),
            fields=None
    ) -> list[Person] | None:
        if fields is None:
            fields = ['full_name']
        items = await self.async_search_db.get_many_with_query_filter_sort_pagination(
            query, index_filter, sort, pagination, fields
        )
        if items:
            return [Person(**item) for item in items]
        return []


@lru_cache()
def get_person_service(
        elastic: AsyncElasticsearch = Depends(get_async_search)
) -> PersonService:
    return PersonService(elastic)
