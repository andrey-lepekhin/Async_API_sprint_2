import datetime
import logging
import os
import time

import psycopg2
from backoff import my_backoff
from db_query import load_film_id
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from ps_to_es import (es_create_genre_index, es_create_person_index,
                      es_create_show_index, generate_actions,
                      generate_genre_actions, generate_person_actions)
from psycopg2.extras import RealDictCursor
from settings import settings
from sqlite_functions import get_lsl_from_sqlite, save_to_sqlite

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


@my_backoff()
def etl_cycle():
    """Класс запуска ETL-цикла"""
    es_client = Elasticsearch(
        hosts=settings.elastic_dsn
    )
    pg_connection = psycopg2.connect(dsn=settings.postgres_dsn, cursor_factory=RealDictCursor)
    try:
        while True:
            main(
                pg_connection=pg_connection,
                es_client=es_client,
                sqlite_db_path=os.environ.get('SQLITE_DB_PATH', 'movies_dmp.sql'),
                frequency=int(os.environ.get('TIME_LOOP', 60)),
            )
    finally:
        logger.info("Разрыв соединения Elasticsearch")
        es_client.transport.close()
        logger.info("Разрыв соединения Postgres")
        pg_connection.close()


@my_backoff()
def main(
        pg_connection: psycopg2.extensions.connection,
        es_client: Elasticsearch,
        sqlite_db_path: str, frequency: int
):
    """
    Метод переноса измененных данных из PG в индекс Elasticsearch

    pg_connection: подключение
    es_client: ES-клиент
    sqlite_db_path: путь до БД
    """
    logger.info('Начало нового цикла')
    last_successful_load = datetime.datetime.fromisoformat(
        get_lsl_from_sqlite(sqlite_db_path)).replace(
        tzinfo=datetime.timezone.utc
    )
    logger.info(f'Последняя загрузка: {last_successful_load}')

    time_since = (datetime.datetime.now(datetime.timezone.utc) -
                  last_successful_load).total_seconds()
    if time_since < frequency:
        logger.info(f'Последний пул был {frequency} секунд назад. Скоро начнется новый')
        time.sleep(frequency - time_since)

    start_time = datetime.datetime.now(datetime.timezone.utc)
    logger.info('Начало загрузки')
    etl_successful = False

    save_to_sqlite(start_time, etl_successful, sqlite_db_path)

    logger.info('Перенос данных в Postgres')
    with pg_connection:
        pg_cursor = pg_connection.cursor()
        pg_cursor.execute(load_film_id)
        logger.debug(pg_cursor.fetchone())
        pg_cursor = pg_connection.cursor()
        # Размер состояния, которое будет передано в Elastic
        pg_cursor.itersize = int(os.environ.get('BULK_SIZE', 1000))

        logger.info('Создание индекса shows')
        es_create_show_index(es_client)
        streaming_blk_shows = streaming_bulk(
            client=es_client,
            index=settings.show_index_name,
            actions=generate_actions(pg_cursor, last_successful_load),
            max_retries=100,
            initial_backoff=0.1,
            max_backoff=10,
        )

        es_create_genre_index(es_client)
        streaming_blk_genres = streaming_bulk(
            client=es_client,
            index=settings.genre_index_name,
            actions=generate_genre_actions(pg_cursor, last_successful_load),
            max_retries=100,
            initial_backoff=0.1,
            max_backoff=10,
        )

        es_create_person_index(es_client)
        streaming_blk_persons = streaming_bulk(
            client=es_client,
            index=settings.person_index_name,
            actions=generate_person_actions(pg_cursor, last_successful_load),
            max_retries=100,
            initial_backoff=0.1,
            max_backoff=10,
        )

        i = 0
        for ok, response in streaming_blk_shows:
            if not ok:
                logger.error('Ошибка при передаче данных shows')
            logger.debug(response)
            i += 1
        for ok, response in streaming_blk_genres:
            if not ok:
                logger.error('Ошибка при передаче данных genres')
            logger.debug(response)
            i += 1
        for ok, response in streaming_blk_persons:
            if not ok:
                logger.error('Ошибка при передаче данных persons')
            logger.debug(response)
            i += 1
        etl_successful = True

    if etl_successful:
        logger.info(f'Перенос завершен успешно. Проведена {i} операция')
    save_to_sqlite(start_time, etl_successful, sqlite_db_path)


if __name__ == '__main__':
    etl_cycle()
