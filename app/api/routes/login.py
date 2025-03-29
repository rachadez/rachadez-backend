from app.api.deps import CurrentUser, SessionDep

from app.api.models import token
from app.api.models.token import Token
from typing import Annotated, Any
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.core import security
from app.core.security import get_password_hash
from app.api.services import login as login_service
from app.api.models.user import UserPublic, NewPassword
from app.api.utils import (
    generate_password_reset_token,
    send_email,
    verify_password_reset_token,
)

from app.api.services import user as user_service

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = login_service.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> str:
    """
    Password Recovery
    """
    user = user_service.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    user_service.dispatch_reset_password_email(email=email, token=password_reset_token)
    return "Password recovery email sent"


@router.post("/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> str:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = user_service.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    return "Password updated successfully"
