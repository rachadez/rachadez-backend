from typing import Any
from datetime import datetime, timezone

from sqlmodel import select, func

from app.core.db import SessionDep
from app.api.models.reservation import Reservation, ReservationResponse, ReservationUsers
from app.api.models.arena import Arena


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


def get_reservations_by_availability_arena_type(session: SessionDep, type_sport: str, offset: int, limit: int) -> Any:
    count_statement = (
        select(func.count())
        .join(Arena, Reservation.arena_id == Arena.id)
        .where(Arena.type_sport == type_sport and 
                Reservation.responsible_id is None and 
                Reservation.end_date < datetime.now(timezone.utc)
                )
        )
    count = session.exec(count_statement).one()
    
    get_statement = (
        select(func.count())
        .join(Arena, Reservation.arena_id == Arena.id)
        .where(Arena.type_sport == type_sport and 
                Reservation.responsible_id is None and 
                Reservation.end_date < datetime.now(timezone.utc)
                )
        ).offset(offset).limit(limit)
    reservations = session.exec(get_statement).all()

    return ReservationResponse(data=list[reservations], count=count)

def get_sport_by_reservation_id(session: SessionDep, reservation: Reservation) -> str:
    query = select(Arena).where(Arena.id == reservation.arena_id)
    arena = session.exec(query).first()

    return arena.type_sport


def get_reservations_by_marked(session:SessionDep, offset: int, limit: int) -> Any:
    count_statement = select(func.count()).where(Reservation.responsible_id is not None and Reservation.end_date > datetime.now(timezone.utc))
    count = session.exec(count_statement).one()

    get_statement = select(Reservation).where(Reservation.responsible_id is not None and Reservation.end_date > datetime.now(timezone.utc)).offset(offset).limit(limit)
    reservations = session.exec(get_statement).all()

    return ReservationResponse(data=list(reservations), count=count)


def get_reservations_by_marked_arena_type(session: SessionDep, type_sport: str, offset: int, limit: int) -> Any:
    count_statement = (
        select(func.count())
        .join(Arena, Reservation.arena_id == Arena.id)
        .where(Arena.type_sport == type_sport and 
                Reservation.responsible_id is not None and 
                Reservation.end_date < datetime.now(timezone.utc)
                )
        )
    count = session.exec(count_statement).one()
    
    get_statement = (
        select(func.count())
        .join(Arena, Reservation.arena_id == Arena.id)
        .where(Arena.type_sport == type_sport and 
                Reservation.responsible_id is not None and 
                Reservation.end_date < datetime.now(timezone.utc)
                )
        ).offset(offset).limit(limit)
    reservations = session.exec(get_statement).all()

    return ReservationResponse(data=list[reservations], count=count) 


def get_last_reservation_from_user(session: SessionDep, user_id: str) -> Reservation | None:
   get_statement = (
       select(Reservation)
       .join(ReservationUsers, ReservationUsers.reservation_id == Reservation.id)
       .where(ReservationUsers.user_id == user_id)
       .order_by(Reservation.end_date.desc())
       .limit(1)
   )
   result = session.exec(get_statement)

   return result.first()
   


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


def add_user_to_reservation(session: SessionDep, user_id: str, reservation_id: str) -> ReservationUsers:
    add_user = ReservationUsers(user_id=user_id, reservation_id=reservation_id)

    session.add(add_user)
    session.commit()
    session.refresh(add_user)

    return add_user
