from typing import Any
from app.core.config import settings
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt


pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_acess_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY)
    return encode_jwt

ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
