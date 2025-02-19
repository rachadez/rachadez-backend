from fastapi import APIRouter

from app.api.routes import example

api_router = APIRouter()

api_router.include_router(example.router)
