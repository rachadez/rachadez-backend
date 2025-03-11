from typing import Annotated, Sequence
import uuid
from fastapi import APIRouter, Query, HTTPException
from app.core.db import SessionDep
from sqlmodel import select
from app.api.models.user import (
    User,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(user: User, session: SessionDep) -> User | None:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/")
def read_users(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> Sequence[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}")
def read_hero(user_id: uuid.UUID, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
