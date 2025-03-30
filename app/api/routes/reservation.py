from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.api.models.user import User
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.api.models.reservation import Reservation, ReservationUpdate
from app.api.services.reservation import create_reservation, delete_reservation, update_reservation
from app.api.models.reservation import ReservationCreate
from app.core.db import get_session

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.post("/", response_model=Reservation)
def create_reservation_route(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db)
    ):
    try:
        reservation = create_reservation(db, reservation_data)
        return reservation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar reserva: {str(e)}")

@router.put("/{reservation_id}", response_model=Reservation)
def update_reservation_route(reservation_id: int, updated_data: ReservationUpdate, db: Session = Depends(get_db)):
    try:
        updated_data_dict = updated_data.model_dump()  
        reservation = update_reservation(db, reservation_id, updated_data_dict)
        return reservation
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao editar a reserva: {str(e)}")
    

@router.delete("/{reservation_id}", response_model=str)
def cancel_reservation_route(
    reservation_id: uuid.UUID,
    user_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    return delete_reservation(db=db, reservation_id=reservation_id, user_id=user_id)


@router.get("/all", response_model=List[Reservation])
def list_all_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Somente administradores podem listar todas as reservas.")
    
    try:
        reservations = db.query(Reservation).all()
        return reservations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar reservas: {str(e)}")
    
@router.get("/{user_id}", response_model=List[Reservation])
def list_user_reservations(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Você só pode ver suas próprias reservas ou ser um administrador.")

    try:
        reservations = db.query(Reservation).filter(Reservation.responsible_user_id == user_id).all()
        return reservations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar reservas do usuário: {str(e)}")