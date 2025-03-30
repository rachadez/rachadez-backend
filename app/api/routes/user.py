from typing import Annotated, Any
import uuid
from pydantic import EmailStr
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.exc import ProgrammingError
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from app.core.security import ALGORITHM
from app.core.config import settings

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

router = APIRouter(tags=["users"])


@router.post(
    "/users/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
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

    user_db = user_service.create_user(session=session, user_create=user_in)
    return user_db


@router.get("/users/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/users/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user_db = user_service.get_user_by_cpf(session=session, cpf=user_in.cpf)
    if user_db:
        raise HTTPException(
            status_code=404, detail="The user with this CPF already exists."
        )

    user = user_service.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    try:
        user = user_service.create_user(session=session, user_create=user_create)
    except HTTPException as e:
        raise e
    except ProgrammingError as e:
        raise e

    return user


@router.get(
    "/users/",
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


@router.get("/users/{user_id}", response_model=UserPublic)
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


@router.get("/users/email/{user_email}", response_model=UserPublic)
def read_user_by_email(
    user_email: EmailStr, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Retrieve a user by email.
    """

    user = user_service.get_user_by_email(email=user_email, session=session)
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
    "/users/{user_id}",
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


@router.delete("/users/{user_id}", dependencies=[Depends(get_current_active_superuser)])
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
@router.get(
    "/block",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[UserPublic],
)
def get_blocked_users(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    """
    Retrieve blocked users.
    """
    users = user_service.get_blocked_users(session=session, offset=offset, limit=limit)
    return users


# Block a user
@router.patch(
    "/block/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=dict,
)
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


@router.patch(
    "/unblock/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
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


@router.get("/users/confirm/{token}", response_model=UserPublic)
def confirm_email(token: str, session: SessionDep):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id = uuid.UUID(payload["sub"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Expired token")
    except InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    session.add(user)
    session.commit()

    return user
