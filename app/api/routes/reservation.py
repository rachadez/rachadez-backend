from typing import Any
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.api.models.reservation import Reservation, ReservationResponse
from app.api.repository import reservation as reservation_repository
from app.core.db import SessionDep

router = APIRouter(prefix="/reservation", tags=["reservation"])

#ADM
@router.post("/")
def create_reservation(session: SessionDep, reservation: Reservation) -> Reservation | None:
    new_reservation = reservation_repository.get_reservation_by_id(session, reservation.id)

    if new_reservation:
        raise HTTPException(
            status_code=404,
            detail="There is already a reservation for ID %s" % reservation.id
        )
    
    new_reservation = reservation_repository(session, reservation)
    return new_reservation

#USER
@router.post("/")
def make_reservation(session: SessionDep, responsible_id: str, reservation_id: str) -> Reservation | None: 
    reservation = reservation_repository.get_reservation_by_id(session, reservation_id)

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="There is no reservation with ID %s" % reservation.id
        )
    if not reservation.responsible_id is None:
        raise HTTPException(
            status_code=404,
            detail="This reservation is already booked"
        )
    new_reservation = Reservation(
        id = reservation.id, 
        responsible_id = reservation.responsible_id, 
        arena_id = reservation.arena_id,
        start_date = reservation.start_date,
        end_date = reservation.end_date,
        made_on = datetime.now(timezone.utc)
        )
    
    reservation_repository.update_reservation(session, reservation, new_reservation)

    return new_reservation


@router.get("/")
def get_reservations(session: SessionDep, offset=0, limit=100) -> Any:
    return reservation_repository.get_reservations(session, offset, limit)


@router.get("/")
def get_reservations_by_availability(session: SessionDep, offset=0, limit=100) -> Any:
    return reservation_repository.get_reservations_by_availability(session, offset, limit)


@router.get("/{id}")
def get_reservation_by_id(session: SessionDep, reservation_id: str) -> Reservation | None:
    reservation = reservation_repository.get_reservation_by_id(session, reservation_id)

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="There is no reservation with ID %s" % reservation_id
        )
    
    return reservation


@router.get("/{arena_id}")
def get_reservations_by_arenaId(session: SessionDep, arena_id: str, offset=0, limit=100) -> Any:
    reservation = reservation_repository.get_reservations_by_arena(session, arena_id, offset, limit)

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="There is no reservation with arena ID %s" % arena_id
        )
    
    return reservation


@router.get("/{responsible_id}")
def get_reservations_by_responsibleId(session: SessionDep, responsible_id: str, offset=0, limit=100) -> Any:
    reservation = reservation_repository.get_reservations_by_responsible(session, responsible_id, offset, limit)

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="There is no reservation with responsible ID %s" % responsible_id
        )


@router.post("/")
def update_reservation(session: SessionDep, reservation_id: str, reservation_update: Reservation) -> Reservation | None:
    reservation = reservation_repository.get_reservation_by_id(session, reservation_id)

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="There is no reservation with ID %s" % reservation_id
        )
    
    updated_reservation = reservation_repository.update_reservation(session, reservation, reservation_update)

    return updated_reservation


@router.delete("/{id}")
def delete_reservation(session: SessionDep, reservation_id: str) -> Reservation | None:
    reservation = reservation_repository.get_reservation_by_id(session, reservation_id)

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="There is no reservation with ID %s" % reservation_id
        )
    
    deleted_reservation = reservation_repository.delete_reservation(session, reservation)

    return deleted_reservation
