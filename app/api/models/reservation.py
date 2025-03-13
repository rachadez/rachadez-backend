from datetime import datetime

from sqlmodel import Field, SQLModel

class Reservation(SQLModel):
    id: str = Field(primary_key=True, max_length=2)
    responsible_id: str = Field(foreign_key='responsible_id', max_length=9)
    arena_id: str = Field(foreign_key='arena_id', max_length=2)
    start_date: datetime
    end_date: datetime


class ReservationResponse(SQLModel):
    data: list[Reservation]
    count: int
