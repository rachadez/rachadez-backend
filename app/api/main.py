from fastapi import APIRouter

from app.api.routes import arena, users, login

api_router = APIRouter()

api_router.include_router(arena.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
