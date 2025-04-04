import uuid
import pytest
from enum import Enum
from app.api.models.user import User
from app.tests.api.base import client, db_session, setup_db
from app.core.security import get_password_hash


class Occupation(str, Enum):
    ALUNO = "ALUNO"
    SERVIDOR = "SERVIDOR"
    PROFESSOR = "PROFESSOR"
    EXTERNO = "EXTERNO"


@pytest.fixture
def setUp(db_session):

    hash_password = get_password_hash("hashed_senha")

    user = User(
    id=uuid.uuid4(),
    email="joao@gmail.com",
    cpf="12345678911",
    phone="83911223344",
    occupation=Occupation.ALUNO, 
    is_active=True,
    is_admin=False,
    is_internal=True,
    full_name="João",
    hashed_password=hash_password,
    reservations=[])
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


class TestLoginRoutes():

    def test_login_access_sucess(self, client, setUp):
        
        response = client.post(
            "/v1/login/access-token",
            data={
                "username": "joao@gmail.com",
                "password": "hashed_senha"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
)


        assert response.status_code == 200, response.text

    def test_login_access_email_not_exists(self, client, setUp):
        
        response = client.post(
            "/v1/login/access-token",
            data={
                "username": "joao123@gmail.com",
                "password": "hashed_senha"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
)


        assert response.status_code == 400, response.text

    def test_login_access_email_exists_with_incorrect_password(self, client, setUp):
        
        response = client.post(
            "/v1/login/access-token",
            data={
                "username": "joao@gmail.com",
                "password": "senha inválida"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
)
        assert response.status_code == 400, response.text