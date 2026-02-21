
import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

def _get_email_credentials():
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    return email_address, email_password

def send_email(to_email, subject, body):
    api_key = os.getenv("BREVO_API_KEY")

    if not api_key:
        raise RuntimeError("Email API key not configured")

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    data = {
        "sender": {"email": os.getenv("EMAIL_ADDRESS")},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": body.replace("\n", "<br>")
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code not in [200, 201]:
        raise RuntimeError(f"Email failed: {response.text}")
