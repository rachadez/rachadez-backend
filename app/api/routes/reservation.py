from fastapi import APIRouter, Depends, HTTPException
from app.api.models.user import User
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.api.models.reservation import Reservation
from app.api.services.reservation import create_reservation
from app.api.models.reservation import ReservationCreate, ReservationResponse

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.post("/", response_model=ReservationResponse)
def create_reservation_route(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Obtendo o usuário atual
):
    # Verificação de tipo de usuário
    if current_user.is_admin:
        # Se o usuário for admin, ele pode fazer qualquer tipo de reserva
        pass
    else:
        # Se o usuário for normal, aplica as regras específicas
        if current_user.is_internal:
            # Usuários internos podem fazer reservas, mas com restrições de horários e esportes
            pass
        else:
            # Usuários externos, verificação de restrições adicionais
            pass

    reservation = Reservation(
        responsible_user_id=current_user.id,  # A reserva será associada ao usuário atual
        arena=reservation_data.arena,
        start_date=reservation_data.start_date,
        end_date=reservation_data.end_date,
        participants=reservation_data.participants  
    )

    new_reservation = create_reservation(db, reservation)
    
    return new_reservation
