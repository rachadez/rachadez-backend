import secrets

class Settings:
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
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost", "http://localhost:5173"]
settings = Settings()