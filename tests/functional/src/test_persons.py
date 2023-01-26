import random
from http import HTTPStatus

import pytest

from tests.functional.testdata.person_bulk import data_persons

pytestmark = pytest.mark.asyncio


async def test_get_all_persons(aiohttp_get, es_with_fresh_indexes) -> None:
    response = await aiohttp_get('persons')
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 10


async def test_search_person(aiohttp_get, es_with_fresh_indexes) -> None:
    random_elem = random.randint(0, len(data_persons)-1)
    data = data_persons[random_elem]
    person_name = data[1].get('full_name')
    person_id = data[1].get('id')
    query = {"query": person_name}
    response = await aiohttp_get(f'persons/search', query)
    assert response.status == HTTPStatus.OK
    assert response.body[0]['full_name'] == person_name
    assert response.body[0]['id'] == person_id


async def test_search_person_from_elastic(aiohttp_get, es_with_fresh_indexes) -> None:
    data = await aiohttp_get('persons')
    for person in random.sample(data.body, 10):
        person_name = person.get('full_name')
        person_id = person.get('id')
        query = {"query": person_name}
        response = await aiohttp_get(f'persons/search', query)
        assert response.status == HTTPStatus.OK
        assert response.body[0]['full_name'] == person_name
        assert response.body[0]['id'] == person_id
