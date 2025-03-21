from app.core.db import SessionDep
from app.api.models.user import User
from sqlmodel import select
from app.core.security import verify_password
from fastapi import HTTPException


def get_user_by_id(session: SessionDep, email: str):
    statement = select(User).where(User.email == email)
    db_user = session.exec(statement).first()
    return db_user

def get_all_users(session: SessionDep):
    statement = select(User)
    return session.exec(statement).all()

def update_password(session: SessionDep, id: str, new_password):
    statement = select(User).where(User.id == id)
    user = session.exec(statement).first()

    if user:
        user.hashed_password = new_password
        session.add(user)
        session.commit()
        session.refresh(user)
    else:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found!")

def authenticate(session: SessionDep, email: str, password: str):
    db_user = get_user_by_id(session, email)
    
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user