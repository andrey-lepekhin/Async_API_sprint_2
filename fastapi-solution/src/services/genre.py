import logging
from functools import lru_cache
from typing import List, Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.dataclasses import Genre
from src.services.utils import get_key_by_args

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5

loggerb = logging.getLogger(__name__)


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def all(self, **kwargs) -> List[Optional[Genre]]:
        genres = await self._genres_from_cache(**kwargs)
        if not genres:
            genres = await self._get_genres_from_elastic(**kwargs)
            if not genres:
                return []
            await self._put_genres_to_cache(genres, **kwargs)
        return genres

    async def _get_genres_from_elastic(self, **kwargs) -> Optional[List[Genre]]:
        page_size = kwargs.get('page_size', 10)
        page = kwargs.get('page', 1)
        sort = kwargs.get('sort', '')
        genre = kwargs.get('genre', None)
        query = kwargs.get('query', None)
        body = None
        if genre:
            body = {
                'query': {
                    'query_string': {
                        'default_field': 'genre',
                        'query': genre
                    }
                }
            }
        if query:
            body = {
                'query': {
                    'match': {
                        'title': {
                            'query': query,
                            'fuzziness': 1,
                            'operator': 'and'
                        }
                    }
                }
            }
        try:
            docs = await self.elastic.search(index='genres',
                                             body=body,
                                             params={
                                                 'size': page_size,
                                                 'from': page - 1,
                                                 'sort': sort,
                                             })
        except NotFoundError:
            loggerb.debug('An error occurred while trying to get genres in ES)')
            return None

        return [await GenreService._make_genre_from_es_doc(doc) for doc in docs['hits']['hits']]

    async def _genres_from_cache(self, **kwargs) -> Optional[List[Genre]]:
        key = await get_key_by_args(**kwargs)
        data = await self.redis.get(key)
        if not data:
            loggerb.debug('Genres was not found in the cache')
            return None

        return [Genre.parse_raw(item) for item in orjson.loads(data)]

    async def _put_genres_to_cache(self, genres: List[Genre], **search_params):
        key = await get_key_by_args(**search_params)
        await self.redis.set(
            key, orjson.dumps([genre.json(by_alias=True) for genre in genres]
                              ),
        )


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
