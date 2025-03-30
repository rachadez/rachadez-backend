import pytest

from app.api.models.arena import Arena, ArenaType
from app.tests.api.base import client, db_session, setup_db


ARENA_PREFIX = "/v1/arenas"


@pytest.fixture
def setUp(db_session):
    arena = Arena(name="Volei1", description="Foo bar",
                  capacity=10, type=ArenaType.VOLEI)
    db_session.add(arena)
    db_session.commit()
    db_session.refresh(arena)

    return arena


class TestArenaRoutes():

    def test_get_arenas(self, client, setUp):
        response = client.get(ARENA_PREFIX + "/")

        assert response.status_code == 200

    def test_get_arena(self, client, setUp):
        response = client.get(ARENA_PREFIX + "/1")

        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Volei1"

    def test_get_arena_not_exists(self, client):
        response = client.get(ARENA_PREFIX + "/1")

        assert response.status_code == 404
        assert "not exists" in response.json()['detail']

    def test_create_arena(self, client):
        data = {"name": "Society Teste",
                "description": "Foo bar", "capacity": 10, "type": "VOLEI"}
        response = client.post(ARENA_PREFIX + "/", json=data)

        created = client.get(ARENA_PREFIX + "/1").json()

        assert response.status_code == 200
        assert created['name'] == data['name']
