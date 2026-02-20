import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(to_email, username):
    subject = "🔥 StreakForge — Your Daily Problem Is Waiting"

    body = f"""
    StreakForge 🚀

    Hi {username},

    Your one problem for today is waiting.
    Don’t lose your streak — consistency beats intensity.
    Even one small step daily builds unstoppable discipline.

    Consistency matters more than motivation.
    Stay sharp. Stay focused.

    — Hariprasad H  
    Founder, StreakForge
    """

    msg = MIMEText(body)
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

    print("✅ Reminder email sent")