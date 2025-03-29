from typing import Annotated
from fastapi import Depends

from sqlmodel import create_engine, select
from sqlmodel import SQLModel, Session

from app.core.config import settings
from app.api.models.user import User, UserCreate, Occupation
from app.api.models.arena import Arena
from app.api.services.user import create_user
from app.api.services.arena import create_arena


# We need to import models so the database can be created by SQLModel
# according to
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters
import app.api.models


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_initial_data():
    with Session(engine) as session:
        init_admin(session)
        init_arenas(session)


def init_admin(session: Session):
    user = session.exec(
        select(User)
        .where(User.email == settings.FIRST_SUPERUSER_EMAIL)).first()

    if not user:
        new_user = UserCreate(email=settings.FIRST_SUPERUSER_EMAIL,
                              password=settings.FIRST_SUPERUSER_PASSWORD,
                              cpf=settings.FIRST_SUPERUSER_CPF,
                              is_admin=True,
                              is_internal=False,
                              occupation=Occupation.SERVIDOR)

        create_user(session=session, user_create=new_user)


def init_arenas(session: Session):
    arenas = settings.ARENAS
    for arena_name in arenas.keys():
        arena = session.exec(select(Arena).where(
            Arena.name == arena_name)).first()

        if not arena:
            new_arena = Arena(
                name=arena_name,
                capacity=arenas[arena_name]['capacity'],
                type=arenas[arena_name]['type'], description="")

            create_arena(session, new_arena)


engine = create_engine(str(settings.DATABASE_URL), echo=True)

SessionDep = Annotated[Session, Depends(get_session)]
