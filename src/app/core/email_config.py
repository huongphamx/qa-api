from pathlib import Path

from fastapi_mail import FastMail, ConnectionConfig
from pydantic import EmailStr, BaseModel

from app.core.config import settings


class EmailSchema(BaseModel):
    email: list[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME=settings.GMAIL_ADDRESS,
    MAIL_PASSWORD=settings.GMAIL_APP_PASSWORD,
    MAIL_FROM=settings.GMAIL_ADDRESS,
    MAIL_PORT=settings.GMAIL_PORT,
    MAIL_SERVER=settings.GMAIL_SMTP_SERVER,
    MAIL_FROM_NAME=settings.GMAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "email-templates",
)

fm = FastMail(conf)
