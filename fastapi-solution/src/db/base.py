from abc import ABC, abstractmethod
from typing import Any


class AsyncFulltextSearch(ABC):
    db: Any

    @abstractmethod
    async def get_by_id(self, index: str, id: str):
        pass

    @abstractmethod
    async def get_many_with_query_filter_sort_pagination(
            self, query, index_filter, sort, pagination, fields
    ):
        pass

    @abstractmethod
    async def close(self):
        pass


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass
