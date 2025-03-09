from fastapi import FastAPI

from app.api.main import api_router
from app.config.config import settings
from app.core.db import Base, engine
from app.models import user
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)

# Create tables automatically
