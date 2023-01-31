import pytest
from elasticsearch import AsyncElasticsearch, Elasticsearch

from functional.settings import test_settings


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