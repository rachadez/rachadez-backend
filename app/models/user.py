from app.core import db
from sqlalchemy import Column, Integer, String, Boolean

print('User model')
class User(db.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    print('User table created')

