from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.main import api_router
from app.core.config import settings
from app.core.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield



app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)
