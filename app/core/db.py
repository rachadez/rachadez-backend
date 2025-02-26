from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print('Passando pelo db.py')
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/postgres'


# Create a session class
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# ORM
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()
print('Base criada')
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()