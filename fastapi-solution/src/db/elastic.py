from elasticsearch import AsyncElasticsearch
from abc import ABC, abstractmethod


class FullTextSearch(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        return es

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass


es: AsyncElasticsearch | None = None


class ESearch(FullTextSearch):

    async def get(self) -> AsyncElasticsearch:
        return es

    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass