from datetime import datetime, timedelta
from app.api.models.arena import Arena
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.api.models.reservation import Reservation
from app.api.models.user import User
from app.core.config import settings
from datetime import time
from sqlalchemy.orm import Session




def send_email(to_email: str, subject: str, content: str):
    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(content, "plain"))

    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
        server.quit()
        print("Email enviado com sucesso AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!")
    except Exception as e:
        print(f"Erro ao enviar email: {e} BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        


def verify_weekly_sports(reservation: Reservation, arena: Arena, user: User) -> bool:

    
    start_date = reservation.start_date

    now = datetime.now()
    today = now.date()
    thursday_15h = today + timedelta(days=(3 - today.weekday() + 7) % 7)
    thursday_15h = datetime.combine(thursday_15h, datetime.min.time()) + timedelta(hours=15)

    if arena.type in ["BEACH_TENNIS", "TÊNIS"]:
        if user.is_internal:
            # Usuários internos podem reservar qualquer horário na semana que estão ou na próxima semana (depois de quinta-feira 15h)
            if start_date.date() >= today:
                return True
            if start_date.date() > today + timedelta(days=7) and now < thursday_15h:
                return False
        else:
            # Usuários externos só podem marcar no fim de semana (sábado e domingo) e dentro dos intervalos de 1h30min
            if start_date.weekday() in [5, 6]:  # Sábado (5) ou Domingo (6)
                valid_times = [
                    time(5, 30), time(7, 0), time(8, 30), time(10, 0), time(11, 30),
                    time(13, 0), time(14, 30), time(16, 0), time(17, 30)
                ]
                if start_date.time() in valid_times and time(5, 30) <= start_date.time() < time(18, 0):
                    return True
            return False
    return True




        
def verify_monthly_sports(reservation: Reservation, arena: Arena, user: User) -> bool:
    
    start_date = reservation.start_date

    now = datetime.now()
    today = now.date()
    
    fifteenth_of_month = today.replace(day=15)
    
    if arena.type in ["VOLEI", "SOCIETY"]:
        if user.is_internal:
            # Usuários internos podem marcar rachas para o mês atual ou o próximo mês após o dia 15
            if start_date.month == today.month:
                return True
            if start_date.month == today.month + 1 or (today.month == 12 and start_date.month == 1):
                if now.date() >= fifteenth_of_month:
                    return True
            return False
        else:
            return False
    


from datetime import datetime, time

from datetime import time

def is_valid_sports_schedule(reservation: Reservation, arena: Arena) -> bool:

    start_time = reservation.start_date.time()
    start_weekday = reservation.start_date.weekday()

    valid_times_weekly = [
        time(5, 30), time(7, 0), time(8, 30), time(10, 0), time(11, 30),
        time(13, 0), time(14, 30), time(16, 0), time(17, 30)
    ]
    valid_times_society = [time(18, 0), time(19, 30)]

    if arena.type in ["BEACH_TENNIS", "TÊNIS", "VOLEI"]:
        if start_weekday < 5:  # Dias úteis (segunda a sexta)
            if time(5, 30) <= start_time < time(21, 0) and start_time in valid_times_weekly:
                return True
        else:  # Finais de semana (sábado e domingo)
            if time(5, 30) <= start_time < time(18, 0) and start_time in valid_times_weekly:
                return True
        return False

    if arena.type == "SOCIETY":
        if start_weekday in [2, 4] and start_time in valid_times_society:  # Quarta ou sexta-feira
            return True
        return False

    return False
  

def is_reservation_available(session: Session, reservation: Reservation) -> bool:
    
    existing_reservation = session.query(Reservation).filter(
        Reservation.arena_id == reservation.arena_id,  
        Reservation.start_date < reservation.end_date,
        Reservation.end_date > reservation.start_date
    ).first()

    return existing_reservation is None 