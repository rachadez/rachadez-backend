from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.models.arena import Arena, ArenaBase, ArenaUpdate
from app.api.repository import arena as arena_repository
from app.core.db import SessionDep


router = APIRouter(prefix="/arenas", tags=["arenas"])


@router.get("/")
def get_arenas(session: SessionDep, offset: int = 0, limit: int = 100) -> Any:
    return arena_repository.get_arenas(session, offset, limit)


@router.get("/{arena_id}")
def get_arena(session: SessionDep, arena_id: int) -> Arena | None:
    arena = arena_repository.get_arena_by_id(session, arena_id)

    if not arena:
        raise HTTPException(
            status_code=404,
            detail="An arena with id %s not exists" % arena_id)

    return arena


@router.post("/")
def create_arena(session: SessionDep, arena: ArenaBase) -> Arena | None:
    new_arena = arena_repository.get_arena_by_name(session, arena)

    if new_arena:
        raise HTTPException(
            status_code=400, detail="An arena with this name already exists")

    new_arena = arena_repository.create_arena(session, arena)

    return new_arena


@router.patch("/{arena_id}")
def update_arena(session: SessionDep, arena_id: int,
                 arena_update: ArenaUpdate) -> Arena | None:
    arena = arena_repository.get_arena_by_id(session, arena_id)

    if not arena:
        raise HTTPException(
            status_code=404,
            detail="An arena with id %s not exists" % arena_id)

    updated_arena = arena_repository.update_arena(session, arena, arena_update)

    return updated_arena


@router.post("/")
def delete_arena():
    pass
