from fastapi import APIRouter

from app.api.routes import example, arena

api_router = APIRouter()

api_router.include_router(example.router)
api_router.include_router(arena.router)
api_router.include_router(reservation.router)