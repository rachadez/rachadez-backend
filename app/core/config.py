import secrets


class Settings:
    API_V1_STR: str = "/v1"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/postgres"
    SECRET_KEY: str = secrets.token_urlsafe(32)


settings = Settings()
