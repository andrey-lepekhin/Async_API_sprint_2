import os
from logging import config as logging_config

from core.logger import LOGGING
from dotenv import find_dotenv, load_dotenv

# Raise error if no .env file found
load_dotenv(find_dotenv(raise_error_if_not_found=False))

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'Practix')

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_V1_BASE_ROUTE = '/api/v1'

SHOW_CACHE_EXPIRE_IN_SECONDS = int(os.getenv('SHOW_CACHE_EXPIRE_IN_SECONDS', 5*60))
SHOW_INDEX_NAME = 'movies' # TODO: change to shows?

SHOW_INDEX_NAME = 'shows'
GENRE_INDEX_NAME = 'genres'

SETTINGS = {
    'refresh_interval': '1s',
    'analysis': {
        'filter': {
            'english_stop': {
                'type': 'stop',
                'stopwords': '_english_',
            },
            'english_stemmer': {
                'type': 'stemmer',
                'language': 'english',
            },
            'english_possessive_stemmer': {
                'type': 'stemmer',
                'language': 'possessive_english',
            },
            'russian_stop': {
                'type': 'stop',
                'stopwords': '_russian_',
            },
            'russian_stemmer': {
                'type': 'stemmer',
                'language': 'russian',
            },
        },
        'analyzer': {
            'ru_en': {
                'tokenizer': 'standard',
                'filter': [
                    'lowercase',
                    'english_stop',
                    'english_stemmer',
                    'english_possessive_stemmer',
                    'russian_stop',
                    'russian_stemmer',
                ],
            },
        },
    },
}
