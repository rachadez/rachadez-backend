import secrets


class Settings:
    PROJECT_NAME: str = "RACHADEZ"
    API_V1_STR: str = "/v1"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/postgres"
    # 60 minutes * 24 hours * 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "rachadez10@gmail.com"
    SMTP_PASSWORD: str = "zvby bxlv ledq takm "
    EMAILS_FROM_NAME: str = "rachadez"
    EMAILS_FROM_EMAIL: str = "rachadez10@gmail.com"
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 1
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    URL_BASE: str = "http://localhost:8000/v1"

    CORS_ORIGINS: list[str] = ["http://localhost", "http://localhost:5173"]

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
            "type": "TÊNIS"
        },
        "Society": {
            "capacity": 10,
            "type": "SOCIETY"
        }}


settings = Settings()
