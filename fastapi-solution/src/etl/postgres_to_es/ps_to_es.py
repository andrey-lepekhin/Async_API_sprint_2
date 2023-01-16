from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from core.config import SHOW_INDEX_NAME, SETTINGS, GENRE_INDEX_NAME
from db_query import full_load


async def es_create_show_index(client):
    """Create shows index in Elasticsearch if one isn't already there."""
    await client.indices.create(
        index=SHOW_INDEX_NAME,
        body={
            'settings': SETTINGS,
            'mappings': {
                'dynamic': 'strict',
                'properties': {
                    'id': {
                        'type': 'keyword',
                    },
                    'imdb_rating': {
                        'type': 'float',
                    },
                    'genre': {
                        'type': 'keyword',
                    },
                    'title': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                        'fields': {
                            'raw': {
                                'type': 'keyword',
                            },
                        },
                    },
                    'description': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                    'director': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                    'actors_names': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                    'writers_names': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                    'actors': {
                        'type': 'nested',
                        'dynamic': 'strict',
                        'properties': {
                            'id': {
                                'type': 'keyword',
                            },
                            'name': {
                                'type': 'text',
                                'analyzer': 'ru_en',
                            },
                        },
                    },
                    'writers': {
                        'type': 'nested',
                        'dynamic': 'strict',
                        'properties': {
                            'id': {
                                'type': 'keyword',
                            },
                            'name': {
                                'type': 'text',
                                'analyzer': 'ru_en',
                            },
                        },
                    },
                },
            },
        },
        ignore=400,
    )


async def es_create_genre_index(client):
    """Create genres index in Elasticsearch if one isn't already there."""
    await client.indices.create(
        index=GENRE_INDEX_NAME,
        body={
            'settings': SETTINGS,
            'mappings': {
                'dynamic': 'strict',
                'properties': {
                    'id': {
                        'type': 'keyword',
                    },
                    'name': {
                        'type': 'str',
                        "analyzer": "ru_en"
                    },
                    'description': {
                        'type': 'str',
                        "analyzer": "ru_en"
                    }
                },
            },
        },
        ignore=400,
    )


class Person(BaseModel):
    id: str
    name: str


class EsDataclass(BaseModel):
    id: str
    underscore_id: str = Field(alias='_id') # публичное имя
    imdb_rating: Optional[float] = None
    genre: Optional[List[str]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    director: Optional[List[str]] = None
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[Person]] = None
    writers: Optional[List[Person]] = None


def validate_row_create_es_doc(row):
    """Метод преобразования данных из PG в ES построчно"""

    def _dict_from_str(string):
        return {
            'id': (string.split(':::'))[0],
            'role': (string.split(':::'))[1],
            'name': (string.split(':::'))[2],
        }

    if row['persons'][0] is not None:
        persons = [_dict_from_str(p) for p in row['persons']]
        directors = [Person(id=p['id'], name=p['name']) for p in persons if p['role'] == 'director']
        actors = [Person(id=p['id'], name=p['name']) for p in persons if p['role'] == 'actor']
        writers = [Person(id=p['id'], name=p['name']) for p in persons if p['role'] == 'writer']
    else:
        directors = actors = writers = []

    return EsDataclass(
        id=row['id'],
        _id=row['id'],
        imdb_rating=row['imdb_rating'],
        genre=row['genre'],
        title=row['title'],
        description=row['description'],
        director=[p.name for p in directors],
        actors_names=[p.name for p in actors],
        writers_names=[p.name for p in writers],
        actors=actors,
        writers=writers,
    ).dict(by_alias=True)


def generate_actions(pg_cursor, last_successful_load):
    """Метод сборки данных об обновленных фильмах"""
    pg_cursor.execute(full_load.format(last_successful_load))
    for row in pg_cursor:
        yield validate_row_create_es_doc(row)
