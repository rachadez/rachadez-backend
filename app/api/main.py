from fastapi import APIRouter

from app.api.routes import example
from app.api.routes import users
from app.api.routes import login

api_router = APIRouter()

api_router.include_router(example.router)
api_router.include_router(users.router)
api_router.include_router(login.router)