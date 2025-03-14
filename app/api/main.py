from fastapi import APIRouter

from app.api.routes import arena, users

api_router = APIRouter()

api_router.include_router(arena.router)
api_router.include_router(users.router)
