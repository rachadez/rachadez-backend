from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped
import uuid

from app.api.models.reservationUserLink import ReservationUserLink





# Modelo Base
class ReservationBase(SQLModel):
    responsible_user_id: Optional[uuid.UUID] = Field(default=None)
    arena_id: int | None = Field(default=None)
    start_date: datetime
    end_date: datetime
    made_on: datetime = Field(default_factory=datetime.utcnow)
    
    

# Modelo de Banco de Dados
class Reservation(ReservationBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    participants: list["User"] = Relationship(back_populates="reservations", link_model=ReservationUserLink)

# Modelo para criação de reserva
class ReservationCreate(SQLModel):
    responsible_user_id: Optional[uuid.UUID]
    arena_id: int 
    start_date: datetime
    end_date: datetime
    participants: List[str] = Field(default=[]) 

class ReservationUpdate(SQLModel):
    start_date: datetime
    end_date: datetime
    participants: List[str] = Field(default=[])