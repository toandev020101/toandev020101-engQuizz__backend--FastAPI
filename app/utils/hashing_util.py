import pyotp
from passlib.context import CryptContext

from app.core import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hotp = pyotp.HOTP(settings.OTP_SECRET_KEY, digits=6)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def generate_otp(version):
    return hotp.at(version)


def verify_otp(otp, version):
    return hotp.verify(otp, version)
