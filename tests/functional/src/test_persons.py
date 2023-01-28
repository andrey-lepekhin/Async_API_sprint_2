import random
from http import HTTPStatus

import pytest


pytestmark = pytest.mark.asyncio


async def test_get_all_persons(aiohttp_get, es_with_fresh_indexes) -> None:
    response = await aiohttp_get('persons')
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 10


async def test_search_person(aiohttp_get, es_with_fresh_indexes, es_client) -> None:
    data = es_client.search(index='persons')
    for person in random.sample(data['hits']['hits'], 10):
        person_name = person['_source']['full_name']
        person_id = person['_source']['id']
        query = {"query": person_name}
        response = await aiohttp_get(f'persons/search', query)
        assert response.status == HTTPStatus.OK
        assert response.body[0]['full_name'] == person_name
        assert response.body[0]['id'] == person_id
