"""United API router for v1"""
from api.v1 import shows, genres
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(shows.router, prefix="/shows", tags=["shows"])
api_router.include_router(genres.router, prefix="/genres", tags=["genres"])
