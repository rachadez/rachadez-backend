from typing import Annotated, Any, Sequence
import uuid
from fastapi import APIRouter, Query, HTTPException, Depends

# from app.core.db import SessionDep
from sqlmodel import select
from app.core import security
from app.api.services import users as user_service
from app.api.models.user import (
    User,
    UserUpdate,
    UserCreate,
    UserPublic,
)

from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
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


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[UserPublic],
)
def read_users(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    """
    Retrieve users.
    """
    users = user_service.read_users(session=session, offset=offset, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Retrieve a user by id.
    """
    # TODO: only admin users can get a user by ID

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return my own user data
    if user == current_user:
        return user

    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
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
