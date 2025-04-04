import pytest

from app.api.models.user import User
from app.tests.api.base import client, db_session, setup_db


USER_PREFIX = "/v1/users"


@pytest.fixture
def setUp(db_session):
    user = User(email="test@example.ufcg.edu.br", cpf="12345678901", hashed_password=)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


class TestArenaRoutes:
    def test_get_arenas(self, client, setUp):
        response = client.get(USER_PREFIX + "/")

        assert response.status_code == 200

    def test_get_arena(self, client, setUp):
        response = client.get(USER_PREFIX + "/1")

        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Volei1"

    def test_get_arena_not_exists(self, client):
        response = client.get(USER_PREFIX + "/1")

        assert response.status_code == 404
        assert "not exists" in response.json()["detail"]

    def test_create_arena(self, client):
        data = {
            "name": "Society Teste",
            "description": "Foo bar",
            "capacity": 10,
            "type": "VOLEI",
        }
        response = client.post(USER_PREFIX + "/", json=data)

        created = client.get(USER_PREFIX + "/1").json()

        assert response.status_code == 200
        assert created["name"] == data["name"]
