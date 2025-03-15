
import secrets

class Settings:
    API_V1_STR: str = "/v1"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/postgres"
    # 60 minutes * 24 hours * 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = secrets.token_urlsafe(32)

    

settings = Settings()
