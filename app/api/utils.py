import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings


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
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

