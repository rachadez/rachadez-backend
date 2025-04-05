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

        assert response.status_code == 200, response.text

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
