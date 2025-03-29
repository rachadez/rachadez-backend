from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

# We need to import models so the database can be created by SQLModel
# according to
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters
import app.api.models

def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



engine = create_engine(str(settings.DATABASE_URL), echo=True)

SessionDep = Annotated[Session, Depends(get_session)]
