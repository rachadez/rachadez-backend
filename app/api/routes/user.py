from typing import Annotated, Any
import uuid
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlmodel import select

from app.api.services import user as user_service
from app.api.models.user import (
    User,
    UserUpdate,
    UserCreate,
    UserPublic,
    UserRegister,
)

from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create_user(user_in: UserCreate, session: SessionDep) -> User | None:
    """
    Create a new user.
    """
    user_db = user_service.get_user_by_cpf(session=session, cpf=user_in.cpf)
    if user_db:
        raise HTTPException(
            status_code=404, detail="The user with this CPF already exists."
        )

    user_db = user_service.get_user_by_email(session=session, email=user_in.email)
    if user_db:
        raise HTTPException(
            status_code=404, detail="The user with this email already exists."
        )
    try:
        user_db = user_service.create_user(session=session, user_create=user_in)
        return user_db
    except HTTPException as e:
        raise e


@router.post("/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = user_service.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = user_service.create_user(session=session, user_create=user_create)
    return user


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


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update_user(user_id: uuid.UUID, user_in: UserUpdate, session: SessionDep):
    """
    Update a user.
    """
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


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
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


# Get users that are blocked
# TODO: only admin can list blocked users
@router.get("/block", response_model=list[UserPublic])
def get_blocked_users(session: SessionDep):
    """
    Retrieve blocked users.
    """
    users = session.exec(select(User).where(not User.is_active)).all()
    return users


# Block a user
# TODO: only admin can blocked
@router.patch("/block/{user_id}", response_model=dict)
def block_user(user_id: uuid.UUID, session: SessionDep):
    """
    Block a user by id.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    session.add(user)
    session.commit()
    return {"ok": True}


@router.patch("/unblock/{user_id}", response_model=UserPublic)
def unblock_user(user_id: uuid.UUID, session: SessionDep):
    """
    Unblock a user by id.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    session.add(user)
    session.commit()
    return user
