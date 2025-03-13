from sqlmodel import SQLModel

class Token(SQLModel):
    acess_token: str
    token_type: str = 'bearer'

class TokenPayload(SQLModel):
    sub: str | None = None