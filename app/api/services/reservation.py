import datetime
from sqlmodel import Session, select
import uuid

import select
from pytest import Session
from fastapi import Depends, HTTPException

from app.api.deps import SessionDep
from app.api.models.reservation import Reservation, ReservationUpdate
from app.api.utils.utils import verify_monthly_sports, verify_weekly_sports, is_valid_sports_schedule, is_reservation_available
from app.api.models.arena import Arena
    
def create_reservation(session: SessionDep, reservation_data: Reservation):

    reservation = Reservation(
        responsible_user_id=reservation_data.responsible_user_id,
        arena=reservation_data.arena_id,
        start_date=reservation_data.start_date,
        end_date=reservation_data.end_date,
        participants=[str(uuid) for uuid in reservation_data.participants],
    )
    arena = session.get(Arena, reservation.arena)
    if not arena:
        raise HTTPException(status_code=400, detail="Arena inválida ou inexistente.")

    if arena.type in ["BEACH_TENNIS", "TÊNIS"]:
        if not verify_weekly_sports(reservation):
            raise HTTPException(status_code=400, detail="Reserva ilegal para este esporte.")
    else:
        if not verify_monthly_sports(reservation):
            raise HTTPException(status_code=400, detail="Reserva ilegal para este esporte.")

    if not is_valid_sports_schedule(reservation):
        raise HTTPException(status_code=400, detail="Reserva ilegal, horário não permitido.")

    
    if not is_reservation_available(session, reservation):
        raise HTTPException(status_code=400, detail="Já existe uma reserva nesse horário.")

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation


def update_reservation(session: Session, reservation_id: int, updated_data: dict):
    
    reservation = session.query(Reservation).filter(Reservation.id == reservation_id).first()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")

    
    for key, value in updated_data.items():
        setattr(reservation, key, value)

    # Verifica se a nova data e horário são válidos
    if not is_valid_sports_schedule(reservation):
        raise HTTPException(status_code=400, detail="Horário inválido para este tipo de arena.")

    # Verificar se o novo horário já está sendo usado
    if not is_reservation_available(session, reservation):
        raise HTTPException(status_code=400, detail="Este horário já está sendo ocupado por outra reserva.")

    # Verificar as regras semanais
    if not verify_weekly_sports(reservation):
        raise HTTPException(status_code=400, detail="Este horário não é válido para reservas semanais.")

    # Verificar as regras mensais
    if not verify_monthly_sports(reservation):
        raise HTTPException(status_code=400, detail="Este horário não é válido para reservas mensais.")

    session.commit()

    return {"message": "Reserva editada com sucesso!"}


def delete_reservation(db: Session, reservation_id: int, user_id: uuid.UUID) -> str:
    
    try:
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()

        if not reservation:
            raise HTTPException(status_code=404, detail="Reserva não encontrada.")

        if reservation.responsible_user_id != user_id:
            raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar esta reserva.")

        if reservation.start_date <= datetime.now():
            raise HTTPException(status_code=400, detail="Não é possível cancelar uma reserva que já iniciou.")

        db.delete(reservation)
        db.commit() 

        return "Reserva cancelada com sucesso."

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor. Por favor, tente novamente. {str(e)}")