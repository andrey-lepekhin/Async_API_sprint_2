import pytest

from tests.functional.settings import test_settings

@pytest.mark.asyncio
async def test_shows_show_id_cache(aiohttp_get, es_async_client, es_with_fresh_indexes) -> None:
    show_id = '00af52ec-9345-4d66-adbe-50eb917f463a'
    endpoint = f'shows/{show_id}'

    response = await aiohttp_get(endpoint)
    assert response.body['id'] == show_id

    await es_async_client.delete(index=test_settings.show_index_name, id=show_id)

    response = await aiohttp_get(endpoint)
    assert response.body['id'] == show_id

#TODO: someday: test cache invalidation
#TODO: in tasks 5, 6, 7, 8: add cache testing for all endpoints.