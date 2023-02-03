import logging
import time
from functools import wraps
from typing import Any

import aioredis
from elasticsearch import Elasticsearch, AsyncElasticsearch

from functional.settings import test_settings

loggerb = logging.getLogger(__name__)


class Backoff:

    def __init__(self, client: Elasticsearch | aioredis.Redis) -> None:
        self.client = client


    def backoff(
            self,
            start_sleep_time=0.1,
            factor=2,
            border_sleep_time=10,
            logger=loggerb
    ) -> Any:
        """
        Function which retry herself when an error occurs.
        Uses the exponential growth of the retry time (factor)
        up to the boundary sleep time (border_sleep_time)
        """

        def func_wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):
                sleep_time = start_sleep_time
                while True:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        logger.error(e)
                        if sleep_time >= border_sleep_time:
                            sleep_time = border_sleep_time
                        else:
                            sleep_time = min(sleep_time * factor, border_sleep_time)
                        time.sleep(sleep_time)

            return inner

        return func_wrapper


class RedisWait(Backoff):

    def __init__(self, client: aioredis.Redis) -> None:
        super().__init__(client)


    def wait_for_redis(self):
        redis = aioredis.from_url(
            test_settings.redis_dsn,
            max_connections=10,
            encoding="utf8",
            decode_responses=True,
        )
        ping = redis.ping()
        if ping:
            return ping
        raise Exception



class ElasticWait(Backoff):

    def __init__(self, client: Elasticsearch) -> None:
        super().__init__(client)


    def wait_for_es(self):
        client = Elasticsearch(
            hosts=test_settings.elastic_dsn,
            ignore_status=[400, 404]
        )
        ping = client.ping()
        if ping:
            return ping
        raise Exception