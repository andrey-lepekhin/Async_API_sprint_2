import random
from http import HTTPStatus

import pytest

from tests.functional.testdata.person_bulk import data_persons

pytestmark = pytest.mark.asyncio
RANDOM_ELEM = random.randint(0, len(data_persons)-1)


@pytest.mark.parametrize(
    'status, endpoint, expected',
    [(200, 'persons', 10)]
)
async def test_get_all_persons(status, endpoint, expected, aiohttp_get, es_with_fresh_indexes) -> None:
    response = await aiohttp_get(endpoint)
    assert response.status == status and len(response.body) == expected


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

