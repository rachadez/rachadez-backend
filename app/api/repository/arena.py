from typing import Any

from sqlmodel import select, func

from app.core.db import SessionDep
from app.api.models.arena import Arena, ArenasPublic, ArenaBase, ArenaUpdate


def create_arena(session: SessionDep, arena: ArenaBase) -> Arena:
    obj = Arena.model_validate(arena)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def get_arena_by_name(session: SessionDep, arena: ArenaBase) -> Arena | None:
    query = select(Arena).where(Arena.name == arena.name)
    session_arena = session.exec(query).first()

    return session_arena


def get_arena_by_id(session: SessionDep, arena_id: int) -> Arena | None:
    query = select(Arena).where(Arena.id == arena_id)
    arena = session.exec(query).first()

    return arena


def get_arenas(session: SessionDep, offset: int, limit: int) -> Any:
    count_statement = select(func.count()).select_from(Arena)
    count = session.exec(count_statement).one()

    get_statement = select(Arena).offset(offset).limit(limit)
    arenas = session.exec(get_statement).all()

    return ArenasPublic(data=list(arenas), count=count)


def update_arena(session: SessionDep, db_arena: Arena,
                 arena_update: ArenaUpdate) -> Arena | None:
    arena_data = arena_update.model_dump(exclude_unset=True)
    db_arena.sqlmodel_update(arena_data)

    session.add(db_arena)
    session.commit()
    session.refresh(db_arena)

    return db_arena
