from functools import lru_cache

from core.config import settings
from db.elastic import get_async_search, AsyncFulltextSearch
from fastapi import Depends
from models.filters import PaginationFilter, QueryFilter
from models.show import Show, ShowGenreFilter, ShowSortFilter
from services.base import BaseService


class ShowService(BaseService):
    def __init__(self, async_search_db: AsyncFulltextSearch):
        self.async_search_db = async_search_db
        self.single_item_model = Show
        self.index_name = settings.service_index_map['show']

    async def get_by_id(self, id: str) -> Show | None:
        item = await self.async_search_db.get_by_id(self.index_name, id)
        if item:
            return self.single_item_model(**item)
        return None

    async def get_many_with_query_filter_sort_pagination(
            self,
            query: QueryFilter = Depends(),
            index_filter: ShowGenreFilter = Depends(),
            sort: ShowSortFilter = Depends(),
            pagination: PaginationFilter = Depends(),
            fields=None
    ) -> list[Show] | None:
        items = await self.async_search_db.get_many_with_query_filter_sort_pagination(
            query, index_filter, sort, pagination, fields
        )
        if items:
            return [Show(**item) for item in items]
        return []


@lru_cache()
def get_show_service(
        async_search_db: AsyncFulltextSearch = Depends(get_async_search)
) -> ShowService:
    return ShowService(async_search_db)
