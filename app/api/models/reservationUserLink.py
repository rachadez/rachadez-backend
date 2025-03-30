

import uuid
from sqlmodel import Field, SQLModel


class ReservationUserLink (SQLModel, table=True):
    user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id", primary_key=True)
    reservation_id: uuid.UUID | None = Field(default=None, foreign_key="reservation.id", primary_key=True)
    