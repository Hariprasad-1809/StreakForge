import smtplib
import os
from pathlib import Path
from email.mime.text import MIMEText
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

def _get_email_credentials():
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    return email_address, email_password

def send_email(to_email, subject, body):
    email_address, email_password = _get_email_credentials()

    if not email_address or not email_password:
        raise RuntimeError("Email credentials are not configured")

    msg = MIMEText(body)
    msg["From"] = email_address
    msg["To"] = to_email
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_address, email_password)
        server.send_message(msg)
