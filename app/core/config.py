import secrets


class Settings():
    API_V1_STR: str = "/v1"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/postgres"

    FIRST_SUPERUSER_EMAIL: str = "admin@complexo.ufcg.edu.br"
    FIRST_SUPERUSER_PASSWORD: str = "adminadmin"
    FIRST_SUPERUSER_CPF: str = "00000000000"

    ARENAS: dict = {
        "Volei de areia 1": {
            "capacity": 10,
            "type": "VOLEI"
        }, "Volei de areia 2": {
            "capacity": 10,
            "type": "VOLEI"
        },
        "Beach Tennis 1": {
            "capacity": 4,
            "type": "BEACH_TENNIS"
        },
        "Beach Tennis 2": {
            "capacity": 4,
            "type": "BEACH_TENNIS"
        },
        "Tenis": {
            "capacity": 4,
            "type": "TENIS"
        },
        "Society": {
            "capacity": 10,
            "type": "SOCIETY"
        }}


settings = Settings()
