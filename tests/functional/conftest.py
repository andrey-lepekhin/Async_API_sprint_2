"""Fixtures"""
import pytest
from elasticsearch import AsyncElasticsearch, Elasticsearch
from tests.functional.settings import test_settings
import aiohttp
from dataclasses import dataclass
from multidict import CIMultiDictProxy
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """A hack from https://stackoverflow.com/a/72104554/196171 prevents 'RuntimeError: Event loop is closed'"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@dataclass
class HTTPResponse:
    status: int
    headers: CIMultiDictProxy[str]
    body: str


@pytest.fixture(scope='session')
async def aiohttp_client_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()

@pytest.fixture
def aiohttp_get(aiohttp_client_session):
    async def inner(
            endpoint: str,
            query: dict = None,
    ):
        url = f'{test_settings.api_service_url}{test_settings.api_v1_base_path}{endpoint}'
        async with aiohttp_client_session.get(url, params=query) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        return HTTPResponse(status=status, headers=headers, body=body)

    return inner

@pytest.fixture(scope='session')
async def es_async_client():
    client = AsyncElasticsearch(hosts=test_settings.elastic_dsn, ignore_status=[400,404])
    yield client
    await client.close()

@pytest.fixture(scope='session')
def es_client():
    client = Elasticsearch(hosts=test_settings.elastic_dsn, ignore_status=[400,404])
    yield client
    client.close()

@pytest.fixture
def make_es_repo(es_client):
    snapshot_body = {
        "type": "fs",
        "settings": {
            "location": "/tmp/test_repo",
            "max_restore_bytes_per_sec": "40mb",
            "readonly": "false",
            "compress": "true",
            "max_snapshot_bytes_per_sec": "40mb"
        }
    }
    es_client.snapshot.create_repository(repository=test_settings.repo_name, body=snapshot_body)

@pytest.fixture
def make_indexes_snapshot(make_es_repo, es_client):
    """
    Is called manually when you want to create a new snapshot to use in tests.
    You might want to use it if you've changed index structure or contents.

    1. Start test ES with `environment: - 'path.repo=/tmp/test_repo/'`
    2. Make indexes and fill them (e.g. with ETL)
    3. Make repo and snapshot with this function
    4. `make elasticsearch` and go into container
    5. `cd /tmp``zip -r indexes_snapshot.zip test_repo` exit container shell
    6. copy file to host `docker cp elasticsearch:/tmp/indexes_snapshot.zip .`, move it to /testdata in repo
    All this in an attempt to isolate test data and not depend on ETL process for it.
    There's gotta be a better way...

    TODO: make `make` command for setting this up
    :param make_es_repo:
    :param es_client:
    :return:
    """

    index_body = {"indices": ','.join(test_settings.index_names)}
    es_client.snapshot.create(repository=test_settings.repo_name, snapshot=test_settings.snapshot_name, body=index_body)

@pytest.fixture
def es_with_fresh_indexes(make_es_repo, es_client):
    def _restore_indexes():
        index_body = {"indices": ','.join(test_settings.index_names)}

        for index in es_client.indices.get(index='*'):
            if index in test_settings.index_names:
                es_client.indices.close(index=index)

        es_client.snapshot.restore(repository=test_settings.repo_name, snapshot=test_settings.snapshot_name, body=index_body)

        for index in es_client.indices.get(index='*'):
            if index in test_settings.index_names:
                es_client.indices.open(index=index)

    _restore_indexes()
    return 'ok'
    # yield
    # _restore_indexes()


