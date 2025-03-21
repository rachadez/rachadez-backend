from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class Reservation(SQLModel):
    id: str = Field(primary_key=True)
    responsible_id: Optional[str] = None 
    arena_id: str 
    start_date: datetime
    end_date: datetime
    made_on: Optional[datetime] = None


class ReservationResponse(SQLModel):
    data: list[Reservation]
    count: int
