from typing import Annotated, Sequence
import uuid
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.db import SessionDep
from sqlmodel import select
from app.api.models.user import (
    User,
)
from app.core import config as settings
from app.core import security
from app.api.repository import user as user_repository
from app.api.models import Token

router = APIRouter(tags=["users"])

#não aceita json
@router.post("/login")
def login(
        session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    )-> Token:
    user = user_repository.authenticate(session=session, email=form_data.username, passoword=form_data.password)

    if not user:
        raise HTTPException(status_code = 400, detail = "Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code = 400, detail = "Inactive user")
    acess_token_expires = timedelta(minutes = settings.ACESSS_TOKEN_EXPIRE_MINUTES)
    return Token(
        acess_token = security.create_acess_token(user.id, expires_delta = acess_token_expires)
    )