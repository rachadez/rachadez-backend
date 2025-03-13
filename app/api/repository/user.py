from app.core.db import SessionDep
from app.api.models.user import User
from sqlmodel import select
from app.core.security import verify_password


def get_user_by_id(session: SessionDep, email: str):
    statement = select(User).where(User.email == email)
    db_user = session.exec(statement).first()
    return db_user


def authenticate(session: SessionDep, email: str, passoword: str):
    db_user = get_user_by_id(session, email)
    
    if not db_user:
        return None
    if not verify_password(email, passoword):
        return None
    return db_user