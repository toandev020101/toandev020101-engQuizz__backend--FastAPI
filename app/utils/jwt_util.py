from datetime import timedelta, datetime
from typing import Optional

from fastapi import Response
from jose import jwt

from app.core import get_settings
from app.models import User

settings = get_settings()


def generate_token(data: dict, secret: str, expires_delta: Optional[timedelta] = None) -> str:
    # Prepare the data to be encoded in the JWT
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"iat": datetime.utcnow()})
    to_encode.update({"exp": expire})

    # Generate and return the JWT token
    encode_jwt = jwt.encode(to_encode, secret, algorithm=settings.ALGORITHM)
    return encode_jwt


def decode_token(token: str) -> dict:
    try:
        # Attempt to decode the token, and check for expiration
        decode_data = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return decode_data if datetime.utcfromtimestamp(decode_data["exp"]) >= datetime.utcnow() else None
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return None
    except jwt.JWTError:
        # Handle other JWT errors
        return {}


def verify_jwt(token: str):
    # Verify the JWT token
    try:
        user_decode = decode_token(token=token)
        return True if user_decode else False
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return False
    except jwt.JWTError:
        # Handle other JWT errors
        return False


def create_access_token(user: User):
    return (generate_token(data={"user_id": user.id, "email": user.email},
                           secret=settings.JWT_SECRET,
                           expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)))


def create_email_token(user: User):
    return (generate_token(data={"user_id": user.id, "email": user.email},
                           secret=settings.EMAIL_SECRET,
                           expires_delta=timedelta(minutes=settings.EMAIL_TOKEN_EXPIRE_MINUTES)))


def send_refresh_token(response: Response, user: User):
    refresh_token = (
        generate_token(
            data={"user_id": user.id, "email": user.email, "token_version": user.token_version},
            secret=settings.JWT_SECRET,
            expires_delta=timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_HOURS)))

    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path=f"{settings.BASE_API_SLUG}/auth/refresh-token"
    )


def clear_refresh_token(response: Response):
    response.delete_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        httponly=True,
        secure=True,
        samesite="lax",
        path=f"{settings.BASE_API_SLUG}/auth/refresh-token"
    )
