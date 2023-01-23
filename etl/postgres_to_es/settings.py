from dotenv import find_dotenv
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    postgres_dsn: PostgresDsn  # E.g. 'postgres://user:pass@localhost:5432/foobar'
    elastic_dsn: str

    show_index_name: str = 'shows'
    genre_index_name: str = 'genres'
    person_index_name: str = 'persons'

    es_common_index_settings: dict = {
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


settings = Settings(_env_file=find_dotenv(), _env_file_encoding='utf-8')
print(settings)