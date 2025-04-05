import pytest
import uuid

from app.api.models.user import User, Occupation
from app.core.security import get_password_hash
from app.tests.api.base import client, db_session, setup_db


USER_PREFIX = "/v1/users"


@pytest.fixture
def setUp(db_session, client):
    user = User(
        full_name="Administrador",
        email="admin@example.ufcg.edu.br",
        cpf="12345678901",
        phone="83911223344",
        occupation=Occupation.SERVIDOR,
        hashed_password=get_password_hash(password="admin password"),
        is_active=True,
        is_admin=True,
        is_internal=True,
        reservations=[],
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


class TestUserRoutes:
    def test_login_access_sucess(self, client, setUp):
        response = client.post(
            "/v1/login/access-token",
            data={
                "username": "admin@example.ufcg.edu.br",
                "password": "admin password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == 200
    

    def test_login_access_incorrect_email(self, client, setUp):
        response = client.post(
            "/v1/login/access-token",
            data={
                "username": "emailerrado@example.ufcg.edu.br",
                "password": "admin password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == 400, response.text
        assert response.json()["detail"] == "Email ou senha incorretos."
    
    def test_login_access_incorrect_password(self, client, setUp):
        response = client.post(
            "/v1/login/access-token",
            data={
                "username": "admin@example.ufcg.edu.br",
                "password": "senha incorreta",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == 400, response.text
        assert response.json()["detail"] == "Email ou senha incorretos."


    def test_get_users(self, client, setUp):
        access_token_response = client.post(
            "/v1/login/access-token",
            data={
                "username": "admin@example.ufcg.edu.br",
                "password": "admin password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        token = access_token_response.json()["access_token"]
        response = client.get(
            USER_PREFIX + "/", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()[0]["email"] == "admin@example.ufcg.edu.br"

    def test_get_user(self, client, setUp):
        access_token_response = client.post(
            "/v1/login/access-token",
            data={
                "username": "admin@example.ufcg.edu.br",
                "password": "admin password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        token = access_token_response.json()["access_token"]
        get_users_response = client.get(
            USER_PREFIX + "/", headers={"Authorization": f"Bearer {token}"}
        )

        first_user_id = get_users_response.json()[0]["id"]

        assert get_users_response.status_code == 200
        response = client.get(
            USER_PREFIX + f"/{first_user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200

    def test_get_user_not_exists(self, client, setUp):
        access_token_response = client.post(
            "/v1/login/access-token",
            data={
                "username": "admin@example.ufcg.edu.br",
                "password": "admin password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        print(access_token_response.json())
        token = access_token_response.json()["access_token"]
        random_uuid = uuid.uuid4()
        response = client.get(
            USER_PREFIX + f"/{random_uuid}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Usuário não encontrado."

    def test_create_internal_user(self, client, setUp):
        data = {
            "email": "user@example.ufcg.edu.br",
            "cpf": "80513586160",
            "phone": "83999124702",
            "occupation": "ALUNO",
            "is_active": True,
            "is_admin": False,
            "is_internal": True,
            "full_name": "Internal User",
            "password": "internal user password",
        }

        access_token_response = client.post(
            "/v1/login/access-token",
            data={
                "username": "admin@example.ufcg.edu.br",
                "password": "admin password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        token = access_token_response.json()["access_token"]

        response = client.post(
            USER_PREFIX + "/",
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json=data,
        )

        assert response.status_code == 200

        get_users_response = client.get(
            USER_PREFIX + "/", headers={"Authorization": f"Bearer {token}"}
        )

        assert len(get_users_response.json()) == 2

        second_user_id = get_users_response.json()[1]["id"]

        created = client.get(
            USER_PREFIX + f"/{second_user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert created.json()["email"] == data["email"]
    
    def test_create_internal_user_email_already_exist(self, client, setUp):
        data = {
            "email": "user@example.ufcg.edu.br",
            "cpf": "12345678911",
            "phone": "83999124702",
            "occupation": "ALUNO",
            "is_active": True,
            "is_admin": False,
            "is_internal": True,
            "full_name": "Internal User",
            "password": "internal user password",
        }

        access_token_response = client.post(
            "/v1/login/access-token",
            data={
                "username": "admin@example.ufcg.edu.br",
                "password": "admin password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        token = access_token_response.json()["access_token"]

        response = client.post(
            USER_PREFIX + "/",
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json=data,
        )

        assert response.status_code == 200

        data_second_user = {
            "email": "user@example.ufcg.edu.br",
            "cpf": "12345678922",
            "phone": "83999124702",
            "occupation": "ALUNO",
            "is_active": True,
            "is_admin": False,
            "is_internal": True,
            "full_name": "Internal User",
            "password": "internal user password",
        }

        response_second_user = client.post(
            USER_PREFIX + "/",
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json=data_second_user,
        )

        assert response_second_user.status_code == 400
        assert response_second_user.json()["detail"] == "Já existe um usuário com esse e-mail."

    def test_create_internal_user_cpf_already_exist(self, client, setUp):
        data = {
            "email": "user@example.ufcg.edu.br",
            "cpf": "12345678911",
            "phone": "83999124702",
            "occupation": "ALUNO",
            "is_active": True,
            "is_admin": False,
            "is_internal": True,
            "full_name": "Internal User",
            "password": "internal user password",
        }

        access_token_response = client.post(
            "/v1/login/access-token",
            data={
                "username": "admin@example.ufcg.edu.br",
                "password": "admin password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        token = access_token_response.json()["access_token"]

        response = client.post(
            USER_PREFIX + "/",
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json=data,
        )

        assert response.status_code == 200

        data_second_user = {
            "email": "user2@example.ufcg.edu.br",
            "cpf": "12345678911",
            "phone": "83999124702",
            "occupation": "ALUNO",
            "is_active": True,
            "is_admin": False,
            "is_internal": True,
            "full_name": "Internal User",
            "password": "internal user password",
        }

        response_second_user = client.post(
            USER_PREFIX + "/",
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json=data_second_user,
        )

        assert response_second_user.status_code == 400
        assert response_second_user.json()["detail"] == "Já existe um usuário com esse CPF."




    def test_signup(self, client, setUp):

        data = {
            "email": "user@ccc.ufcg.edu.br",
            "password": "senha1234",
            "cpf": "12345678911",
            "phone": "83911223344",
            "occupation": "ALUNO",
            "full_name": "user"
        }

        response = client.post(
            USER_PREFIX + "/signup",
            json=data
        )

        assert response.status_code == 200
        assert data["email"] == response.json()["email"]
        assert "id" in response.json()
    
    def test_singup_user_email_already_exist(self, client, setUp):

        data = {
            "email": "user@ccc.ufcg.edu.br",
            "password": "senha1234",
            "cpf": "11111111111",
            "phone": "83911111111",
            "occupation": "ALUNO",
            "full_name": "user"
        }

        response = client.post(
            USER_PREFIX + "/signup",
            json=data
        )

        assert response.status_code == 200

        data2 = {
            "email": "user@ccc.ufcg.edu.br",
            "password": "senha1234",
            "cpf": "22222222222",
            "phone": "83922222222",
            "occupation": "ALUNO",
            "full_name": "user"
        }

        response2 = client.post(
            USER_PREFIX + "/signup",
            json=data2
        )

        assert response2.status_code == 400
        assert response2.json()["detail"] == "Já existe um usuário com esse e-mail."
    
    def test_singup_user_cpf_already_exist(self, client, setUp):

        data = {
            "email": "user@ccc.ufcg.edu.br",
            "password": "senha1234",
            "cpf": "11111111111",
            "phone": "83911111111",
            "occupation": "ALUNO",
            "full_name": "user"
        }

        response = client.post(
            USER_PREFIX + "/signup",
            json=data
        )

        assert response.status_code == 200

        data2 = {
            "email": "user2@ccc.ufcg.edu.br",
            "password": "senha1234",
            "cpf": "11111111111",
            "phone": "83922222222",
            "occupation": "ALUNO",
            "full_name": "user"
        }

        response2 = client.post(
            USER_PREFIX + "/signup",
            json=data2
        )

        assert response2.status_code == 400
        assert response2.json()["detail"] == "Já existe um usuário com esse CPF."

    def test_singup_user_invalid_cpf1(self, client): 

        data = {
            "email" : "user@ccc.ufcg.edu.br",
            "password" : "senha1234",
            "cpf" : "123456789123", # invalid CPF (more than 11 digits)
            "phone" : "83911111111",
            "occupation" : "ALUNO",
            "full_name" : "CPF inválido"
        }

        response = client.post(
            USER_PREFIX + "/signup",
            json=data
        )


        assert response.status_code == 422  # Validation error
        response_data = response.json()["detail"]

        assert any(
            error["loc"] == ["body", "cpf"] and
            error["msg"] == "String should have at most 11 characters"
            for error in response_data
        )






