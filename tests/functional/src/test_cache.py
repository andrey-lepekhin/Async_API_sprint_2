import uuid
from http import HTTPStatus
from time import sleep

import pytest

from tests.functional.settings import test_settings

pytestmark = pytest.mark.asyncio


async def test_shows_show_id_cache(aiohttp_get, es_async_client, es_with_fresh_indexes) -> None:
    show_id = '00af52ec-9345-4d66-adbe-50eb917f463a'
    endpoint = f'shows/{show_id}'

    response = await aiohttp_get(endpoint)
    assert response.body['id'] == show_id

    await es_async_client.delete(index=test_settings.show_index_name, id=show_id)

    response = await aiohttp_get(endpoint)
    assert response.body['id'] == show_id


@pytest.mark.parametrize(
    'person_id',
    [
        '6e429cff-c8a2-4d17-8b12-6532a8a1ac9b',
        'bbdbad95-f08b-4e12-ba35-92b89c9251f8',
        'efa1894b-0384-4164-b55d-424980142c28'
     ]
)
async def test_persons_cache_pass(person_id, aiohttp_get, es_async_client, es_with_fresh_indexes) -> None:
    endpoint = f'persons/{person_id}'
    response = await aiohttp_get(endpoint)
    assert response.body['id'] == person_id

    await es_async_client.delete(index=test_settings.person_index_name, id=person_id)

    response = await aiohttp_get(endpoint)
    assert response.body['id'] == person_id


@pytest.mark.parametrize(
    'person_id',
    [
        '6e429cff-c8a2-4d17-8b12-6532a8a1ac9b',
        'bbdbad95-f08b-4e12-ba35-92b89c9251f8',
        'efa1894b-0384-4164-b55d-424980142c28'
     ]
)
async def test_persons_cache_expiration(
        person_id, aiohttp_get, es_async_client, es_with_fresh_indexes
) -> None:
    endpoint = f'persons/{person_id}'
    response = await aiohttp_get(endpoint)
    assert response.body['id'] == person_id

    await es_async_client.delete(index=test_settings.person_index_name, id=person_id)
    sleep(70)

    with pytest.raises(KeyError):
        response = await aiohttp_get(endpoint)
        assert response.body['id'] == person_id

#TODO: someday: test cache invalidation
#TODO: in tasks 5, 6, 7, 8: add cache testing for all endpoints.