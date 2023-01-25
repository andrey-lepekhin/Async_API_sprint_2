import pytest
from tests.functional.settings import test_settings
import asyncio


@pytest.mark.asyncio
async def test_search(aiohttp_get, es_with_fresh_indexes) -> None:
    endpoint = 'shows/search'
    query_data = {'query': 'The Star'}
    response = await aiohttp_get(endpoint, query_data)
    assert response.status == 200
    assert response.body[0]['id'] == '05d7341e-e367-4e2e-acf5-4652a8435f93'


@pytest.mark.asyncio
async def test_cache(aiohttp_get, es_async_client, es_with_fresh_indexes):
    show_id = '00af52ec-9345-4d66-adbe-50eb917f463a'
    endpoint = f'shows/{show_id}'

    response = await aiohttp_get(endpoint)
    assert response.body['id'] == show_id

    await es_async_client.delete(index=test_settings.show_index_name, id=show_id)

    response = await aiohttp_get(endpoint)
    assert response.body['id'] == show_id


