from typing import Annotated
import uuid
from fastapi import APIRouter, Query, HTTPException
from app.core.db import SessionDep
from sqlmodel import select
from app.api.services import users as user_service
from app.api.models.user import (
    User,
    UserUpdate,
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

#Get users that are blocked
#TODO: only admin can list blocked users
@router.get("/blocked_users", response_model=list[UserPublic])
def get_blocked_users(session: SessionDep):
    users = session.exec(select(User).where(User.is_active == False)).all()
    return users

@router.get("/", response_model=list[UserPublic])
def read_users(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
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
def update_user(user_id: uuid.UUID, user_in: UserUpdate, session: SessionDep):
    """
    Update a user.
    """
    # TODO: only admin users can update a user by ID
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist",
        )
    if user_in.email:
        existing_user = user_service.get_user_by_email(
            session=session, email=user_in.email
        )
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = user_service.update_user(
        session=session, db_user=db_user, user_in=user_in
    )
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID, session: SessionDep):
    """
    Delete a user.
    """
    # TODO: only admin users can delete a user by ID
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

# Block a user
# TODO: only admin can blocked
@router.patch("/block/{user_id}", response_model=dict)
def block_user(user_id: uuid.UUID, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    session.add(user)
    session.commit() 
    return {"ok":True}

@router.patch("/unblock/{user_id}", response_model=dict)
def unblock_user(user_id: uuid.UUID, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    session.add(user)
    session.commit()
    return {"ok":True}