import logging
from logging import config as logging_config

from core.logger import LOGGING
from dotenv import find_dotenv
from pydantic import BaseSettings, RedisDsn

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str = 'Practix'

    # Настройки Redis
    redis_dsn: RedisDsn

    # Настройки Elasticsearch
    elastic_dsn: str

    log_level: int = logging.DEBUG
    logging_config: dict = LOGGING

    server_host: str
    server_port: str

    api_v1_base_route: str = '/api/v1'

    cache_expiration_in_seconds: int

    show_index_name: str = 'shows'
    genre_index_name: str = 'genres'
    person_index_name: str = 'persons'


settings = Settings(_env_file=find_dotenv(), _env_file_encoding='utf-8')
