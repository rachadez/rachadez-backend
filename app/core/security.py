from typing import Any
from app.core.db import SessionDep
import app.core.security as settings
from app.api.models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt



pwd_context = CryptContext(schemes = ['bcripty'], deprecated = 'auto')

def verify_password(email: str, password: str):
    return pwd_context.verify(email, password)


def create_acess_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_ecode = {"exp": expire, "sub": str(subject)}
    encode_jwt = jwt.encode(to_ecode, settings.SECRETE_KEY)

