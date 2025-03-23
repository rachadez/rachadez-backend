from enum import Enum

from sqlmodel import Field, SQLModel


class ArenaType(str, Enum):
    VOLEI = "VOLEI"
    BEACH_TENNIS = "BEACH_TENNIS"
    SOCIETY = "SOCIETY"
    TENIS = "TÊNIS"


class ArenaBase(SQLModel):
    name: str
    description: str
    capacity: int
    type: ArenaType


class Arena(ArenaBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ArenasPublic(SQLModel):
    data: list[Arena]
    count: int


class ArenaUpdate(ArenaBase):
    name: str = Field(default=None)
    description: str = Field(default=None)
    capacity: int = Field(default=None)
