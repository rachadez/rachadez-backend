from typing import Annotated, Sequence
import uuid
from fastapi import APIRouter, Query, HTTPException
from app.core.db import SessionDep
from sqlmodel import select
from api.services import users as user_service
from app.api.models.user import (
    User,
    UserUpdate,
    UsersPublic,
    UserCreate,
    UserPublic,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic)
def create_user(user_in: UserCreate, session: SessionDep) -> User | None:
    """
    Create a new user.
    """
    user_db = user_service.get_user_by_email(session=session, email=user_in.email)
    if user_db:
        raise HTTPException(
            status_code=404, detail="The user with this email already exists."
        )
    user_db = user_service.create_user(session=session, user_create=user_in)
    return user_db


@router.get("/", response_model=UsersPublic)
def read_users(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> Sequence[User]:
    """
    Retrieve users.
    """
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: uuid.UUID, session: SessionDep) -> User:
    """
    Retrieve a user by id.
    """
    # TODO: only admin users can get a user by ID
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id: uuid.UUID, user: UserUpdate, session: SessionDep):
    """
    Update a user.
    """
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID, session: SessionDep):
    """
    Delete a user.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
