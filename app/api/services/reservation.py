
from multiprocessing.heap import Arena
from app.api.deps import SessionDep
from app.api.models.reservation import Reservation
from app.api.utils.utils import verify_monthly_sports, verify_weekly_sports, is_valid_sports_schedule, is_reservation_available
from fastapi import HTTPException

    
def create_reservation(session: SessionDep, reservation: Reservation):
    """Cria uma reserva validando todas as regras do sistema."""

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