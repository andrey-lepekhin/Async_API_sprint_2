import pytest


pytestmark = pytest.mark.asyncio


async def test_shows_search(aiohttp_get, es_with_fresh_indexes) -> None:
    endpoint = 'shows/search'
    query_data = {'query': 'The Star'}
    response = await aiohttp_get(endpoint, query_data)
    assert response.status == 200
    assert response.body[0]['id'] == '05d7341e-e367-4e2e-acf5-4652a8435f93'


@pytest.mark.parametrize(
    'status, endpoint, query_data, id_index',
    [
        (200, 'persons/search', {'query': 'Václav Vorlícek'}, '6e429cff-c8a2-4d17-8b12-6532a8a1ac9b')
     ]
)
async def test_search_person(status, endpoint, query_data, id_index, aiohttp_get, es_with_fresh_indexes) -> None:
    response = await aiohttp_get(endpoint, query_data)
    assert response.status == status and response.body[0]['id'] == id_index
