from typing import Any
from datetime import datetime, timezone

from sqlmodel import select, func

from app.core.db import SessionDep
from app.api.models.reservation import Reservation, ReservationResponse


def create_reservation(session: SessionDep, reservation: Reservation) -> Reservation:
    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation


def get_reservations(session: SessionDep, offset: int, limit: int) -> Any:
    count_statement = select(func.count()).select_from(Reservation)
    count = session.exec(count_statement).one()

    get_statement = select(Reservation).offset(offset).limit(limit)
    reservations = session.exec(get_statement).all()

    return ReservationResponse(data=list(reservations), count=count)


def get_reservations_by_arena(session: SessionDep, arena_id: str, offset: int, limit: int) -> Any:
    count_statement = select(func.count()).where(Reservation.arena_id == arena_id)
    count = session.exec(count_statement).one()

    get_statement = select(Reservation).where(Reservation.arena_id == arena_id).offset(offset).limit(limit)
    reservations = session.exec(get_statement).all()
    
    return ReservationResponse(data=list(reservations), count=count)


def get_reservations_by_responsible(session: SessionDep, responsible_id: str, offset: int, limit: int) -> Any:
    count_statement = select(func.count()).where(Reservation.responsible_id == responsible_id)
    count = session.exec(count_statement).one()

    get_statement = select(Reservation).where(Reservation.responsible_id == responsible_id).offset(offset).limit(limit)
    reservations = session.exec(get_statement).all()
    
    return ReservationResponse(data=list(reservations), count=count)


def get_reservation_by_id(session: SessionDep, reservation_id: str) -> Reservation | None:
    query = select(Reservation).where(Reservation.id == reservation_id)
    reservation = session.exec(query).first()

    return reservation


def get_reservations_by_availability(session: SessionDep, offset: int, limit: int) -> Any:
    count_statement = select(func.count()).where(Reservation.responsible_id is None and Reservation.end_date > datetime.now(timezone.utc))
    count = session.exec(count_statement).one()

    get_statement = select(Reservation).where(Reservation.responsible_id is None and Reservation.end_date > datetime.now(timezone.utc)).offset(offset).limit(limit)
    reservations = session.exec(get_statement).all()

    return ReservationResponse(data=list(reservations), count=count)


def get_reservations_by_marked(session:SessionDep, offset: int, limit: int) -> Any:
    count_statement = select(func.count()).where(Reservation.responsible_id is not None and Reservation.end_date > datetime.now(timezone.utc))
    count = session.exec(count_statement).one()

    get_statement = select(Reservation).where(Reservation.responsible_id is not None and Reservation.end_date > datetime.now(timezone.utc)).offset(offset).limit(limit)
    reservations = session.exec(get_statement).all()

    return ReservationResponse(data=list(reservations), count=count)


def delete_reservation(session: SessionDep, reservation: Reservation) -> Reservation | None:
    session.delete(reservation)
    session.commit()
    
    return reservation


def update_reservation(session: SessionDep, db_reservation: Reservation, update_reservation: Reservation) -> Reservation | None:
    reservation_data = update_reservation.model_dump(exclude_unset=True)
    db_reservation.sqlmodel_update(reservation_data)

    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)

    return db_reservation

