from http import HTTPStatus

import pytest


pytestmark = pytest.mark.asyncio


async def test_shows_search(aiohttp_get, es_with_fresh_indexes) -> None:
    endpoint = 'shows/search'
    query_data = {'query': 'The Star'}
    response = await aiohttp_get(endpoint, query_data)
    assert response.status == HTTPStatus.OK
    assert response.body[0]['id'] == '05d7341e-e367-4e2e-acf5-4652a8435f93'
    #TODO: don't hardcode id but get random items from elastic


@pytest.mark.parametrize(
    'endpoint, query_data, id_index',
    [
        ('persons/search', {'query': 'Václav Vorlícek'}, '6e429cff-c8a2-4d17-8b12-6532a8a1ac9b')
     ]
)
async def test_search_person(endpoint, query_data, id_index, aiohttp_get, es_with_fresh_indexes) -> None:
    response = await aiohttp_get(endpoint, query_data)
    assert response.status == HTTPStatus.OK
    assert response.body[0]['id'] == id_index


@pytest.mark.parametrize(
    'endpoint, id_index',
    [
        ('genres', 'eb7212a7-dd10-4552-bf7b-7a505a8c0b95')
     ]
)
async def test_search_genre(endpoint, id_index, aiohttp_get, es_with_fresh_indexes) -> None:
    response = await aiohttp_get(f'{endpoint}/{id_index}')
    assert response.status == HTTPStatus.OK
    assert response.body['id'] == id_index
