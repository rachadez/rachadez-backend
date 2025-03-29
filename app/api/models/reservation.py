from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
import uuid

# Tabela de Associação entre Reservation e User
class ReservationUserAssociation(SQLModel, table=True):
    reservation_id: int = Field(foreign_key="reservation.id", primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)  # Alterado para UUID

# Base para modelos compartilhados
class ReservationBase(SQLModel):
    responsible_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")  # Alterado para UUID
    arena: int | None = Field(default=None, foreign_key="arena.id")
    start_date: datetime
    end_date: datetime
    made_on: datetime = Field(default_factory=datetime.utcnow)

# Modelo de Banco de Dados (herda ReservationBase e define que é uma tabela)
class Reservation(ReservationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    participants: List["User"] = Relationship(back_populates="reservations", link_model=ReservationUserAssociation)

class ReservationCreate(SQLModel):
    """Schema para criação de reservas"""
    responsible_user_id: Optional[uuid.UUID]  # Alterado para UUID
    arena: int  # ID da arena reservada
    start_date: datetime  # Data/hora de início da reserva
    end_date: datetime  # Data/hora de término da reserva
    participants: List[uuid.UUID]  # Lista de IDs dos usuários participantes (alterado para UUID)

class ReservationResponse(SQLModel):
    """Schema para resposta da API ao criar uma reserva"""
    id: int  # ID da reserva gerada
    responsible_user_id: uuid.UUID  # Alterado para UUID
    arena: int  # ID da arena reservada
    start_date: datetime
    end_date: datetime
    made_on: datetime  # Data/hora em que a reserva foi feita
    participants: List[uuid.UUID]  # Lista de IDs dos participantes (alterado para UUID)
