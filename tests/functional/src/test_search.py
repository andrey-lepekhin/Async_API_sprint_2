import asyncio

import pytest

from tests.functional.settings import test_settings


@pytest.mark.asyncio
async def test_shows_search(aiohttp_get, es_with_fresh_indexes) -> None:
    endpoint = 'shows/search'
    query_data = {'query': 'The Star'}
    response = await aiohttp_get(endpoint, query_data)
    assert response.status == 200
    assert response.body[0]['id'] == '05d7341e-e367-4e2e-acf5-4652a8435f93'

#TODO: in task 8: rest of the search tests