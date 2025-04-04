from datetime import datetime
from sqlmodel import Session, select
import uuid
from fastapi import Depends, HTTPException

from app.api.deps import CurrentUser, SessionDep
from app.api.models.reservationUserLink import ReservationUserLink
from app.api.models.reservation import Reservation, ReservationCreate, ReservationUpdate
from app.api.models.user import User
from app.api.utils.utils import verify_monthly_sports, verify_weekly_sports, is_valid_sports_schedule, is_reservation_available, verify_end_date
from app.api.models.arena import Arena
    
def create_reservation(session: SessionDep, reservation_data: ReservationCreate):
    
    try:
        # Buscar usuários participantes
        lista_de_usuarios = []
        for user_uuid in reservation_data.participants:
            usuario = session.exec(select(User).filter(User.id == user_uuid)).first()
            if usuario:
                lista_de_usuarios.append(usuario)
            
        # Criar a reserva
        reservation = Reservation(
            responsible_user_id=reservation_data.responsible_user_id,
            arena_id=reservation_data.arena_id,
            start_date=reservation_data.start_date,
            end_date=reservation_data.end_date,
            participants=lista_de_usuarios,
        )
        
        # Verificar a arena e o usuário responsável
        arena = session.get(Arena, reservation.arena_id)
        user = session.get(User, reservation.responsible_user_id)
        
        #if not is_previous_week(user.last_reservation):
        #    raise HTTPException(status_code=400, detail="Esse Usuario ainda não esta disponivel para fazer uma reserva")
        
        if not arena:
            raise HTTPException(status_code=400, detail="Arena inválida ou inexistente.")
        
        if not verify_end_date(reservation.start_date, reservation.end_date):
            raise HTTPException(status_code=400, detail="Horario de inicio e fim Invalidos")
        
        if arena.type in ["BEACH_TENNIS", "TÊNIS"]:
            if not verify_weekly_sports(reservation, arena, user):
                raise HTTPException(status_code=400, detail="Reserva ilegal para este esporte.")
        else:
            if not verify_monthly_sports(reservation, arena, user):
                raise HTTPException(status_code=400, detail="Reserva ilegal para este esporte.")
        
        if not is_valid_sports_schedule(reservation, arena):
            raise HTTPException(status_code=400, detail="Reserva ilegal, horário ou data não permitido.")
        
        if not is_reservation_available(session, reservation):
            raise HTTPException(status_code=400, detail="Já existe uma reserva nesse horário.")
        
        # Adicionar e persistir a reserva
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        
        return reservation
    
    except HTTPException as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar reserva: {str(e)}")
    


def update_reservation(session: Session, reservation_id: int, updated_data: ReservationUpdate, user: User):
    
    reservation = session.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation.responsible_user_id ==  user.id:
        raise HTTPException(status_code=500, detail="Usuario autenticado incorreto")
        
    lista_de_usuarios = []
    for uuid in updated_data.participants:
        usuario = session.exec(select(User).filter(User.id == uuid)).first()
        if usuario:
            lista_de_usuarios.append(usuario)
    reservation_update= {
        "start_date": updated_data.start_date,
        "end_date": updated_data.end_date,
        "participants": lista_de_usuarios,
    }
    
    arena = session.get(Arena, reservation.arena_id)
    user = session.get(User, reservation.responsible_user_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")

    
    for key, value in reservation_update.items():
        if value:
            setattr(reservation, key, value)

    if not verify_end_date(reservation.start_date, reservation.end_date):
            raise HTTPException(status_code=400, detail="Horario de inicio e fim Invalidos")
    
    # Verifica se a nova data e horário são válidos
    if not is_valid_sports_schedule(reservation, arena):
        raise HTTPException(status_code=400, detail="Horário inválido para este tipo de arena.")

    # Verificar se o novo horário já está sendo usado
    if is_reservation_available(session, reservation):
        raise HTTPException(status_code=400, detail="Este horário já está sendo ocupado por outra reserva.")

    if not verify_weekly_sports(reservation, arena, user):
        raise HTTPException(status_code=400, detail="Este horário não é válido para reservas semanais.")
    elif not verify_monthly_sports(reservation, arena, user):
        raise HTTPException(status_code=400, detail="Este horário não é válido para reservas mensais.")

    session.add(reservation)
    session.commit()
    session.refresh(reservation)


    return reservation


def delete_reservation(db: Session, reservation_id: uuid.UUID, user_id: uuid.UUID, user: User) -> str:
    
    try:
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()

        if not reservation:
            raise HTTPException(status_code=404, detail="Reserva não encontrada.")

        if reservation.responsible_user_id != user_id and not user.is_admin:
            raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar esta reserva.")

        if reservation.start_date <= datetime.now():
            raise HTTPException(status_code=400, detail="Não é possível cancelar uma reserva que já iniciou.")

        db.delete(reservation)
        db.commit() 

        return "Reserva cancelada com sucesso."

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor. Por favor, tente novamente. {str(e)}")
    

def get_participants_by_reservation_id(session: Session,reservation_id: uuid.UUID):
    participants = []
    
    users = session.query(ReservationUserLink.user_id).filter(ReservationUserLink.reservation_id == reservation_id).all()
    
    for value in users:
        user = session.get(User, value)
        if user:
            participants.append(user)
            
    return participants