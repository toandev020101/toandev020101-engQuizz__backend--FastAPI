import os
from typing import List, Dict

from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from pydantic import EmailStr

from app.core import get_settings
from app.enums import EmailEnum

settings = get_settings()

subjects = {
    'verify': "Email xác minh tài khoản EngQuizz",
    'reset_password': "Email đặt lại mật khẩu tài khoản EngQuizz"
}

bodies = {
    "verify": "verify_email_template.html",
    'reset_password': "reset_password_template.html"
}

dir_path = os.path.dirname(os.path.dirname(__file__))
templates = Jinja2Templates(directory=f"{dir_path}/templates")


async def send_email(email_type: EmailEnum, emails: List[EmailStr], data: Dict[str, str]):
    template = templates.get_template(
        bodies.get(email_type.name.lower()))

    body_html = template.render(**data)

    message = MessageSchema(
        subject=subjects.get(email_type.name.lower()),
        recipients=emails,
        body=body_html,
        subtype='html'
    )

    fm = FastMail(config=ConnectionConfig(
        MAIL_USERNAME=settings.EMAIL_USERNAME,
        MAIL_PASSWORD=settings.EMAIL_PASSWORD,
        MAIL_FROM=settings.EMAIL_USERNAME,
        MAIL_PORT=settings.EMAIL_PORT,
        MAIL_SERVER=settings.EMAIL_SERVER,
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    ))
    await fm.send_message(message=message)
