from app.api.models.Token import Token
from typing import Annotated, Sequence
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.db import SessionDep
from app.core.config import settings
from app.core import security
from app.api.repository import user as user_repository

router = APIRouter(tags=["users"])

@router.post("/login")
def login(
        session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    )-> Token:
    user = user_repository.authenticate(session=session, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code = 400, detail = "Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code = 400, detail = "Inactive user")
    access_token_expires = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token = security.create_acess_token(user.id, expires_delta = access_token_expires)
    )