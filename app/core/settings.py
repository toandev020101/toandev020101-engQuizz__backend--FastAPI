import os
from datetime import date
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # App
    APP_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_ROOT: str = os.path.join(os.path.dirname(APP_ROOT), "uploads")

    APP_NAME: str = os.environ.get("APP_NAME", "FastAPI")
    APP_DESCRIPTION: str = os.environ.get("APP_DESCRIPTION", "")
    APP_VERSION: str = os.environ.get("APP_VERSION", "0.1.0")
    APP_HOST: str = os.environ.get("APP_HOST", "localhost")
    APP_PORT: int = os.environ.get("APP_PORT", 8000)

    CLIENT_URL: str = os.environ.get("CLIENT_URL", "http://localhost")
    SERVER_URL: str = f"http://{APP_HOST}:{APP_PORT}"
    BASE_API_SLUG: str = os.environ.get("BASE_API_SLUG", "/v1/api")
    DEBUG: bool = bool(os.environ.get("DEBUG", False))

    # Postgresql Database Config
    POSTGRESQL_HOST: str = os.environ.get("POSTGRESQL_HOST", 'localhost')
    POSTGRESQL_USER: str = os.environ.get("POSTGRESQL_USER", 'root')
    POSTGRESQL_PASS: str = os.environ.get("POSTGRESQL_PASSWORD", 'secret')
    POSTGRESQL_PORT: int = int(os.environ.get("POSTGRESQL_PORT", 5432))
    POSTGRESQL_DB: str = os.environ.get("POSTGRESQL_DB", 'fastapi')
    DATABASE_URI: str = f"postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASS}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DB}"

    # App Secret Key
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")

    # JWT Secret
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "649fb93ef34e4fdf4187709c84d643dd61ce730d91856418fdcf563f895ea40f")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    REFRESH_TOKEN_EXPIRE_HOURS: int = os.environ.get("REFRESH_TOKEN_EXPIRE_HOURS", "5")
    REFRESH_TOKEN_COOKIE_NAME: str = os.environ.get("REFRESH_TOKEN_COOKIE_NAME", "fastapi_cookie")

    # OPA
    OPA_URL: str = os.environ.get("OPA_URL", "http://localhost:8181/v1/data/authz")

    # EMAIL
    EMAIL_TOKEN_EXPIRE_MINUTES: int = os.environ.get("EMAIL_TOKEN_EXPIRE_MINUTES", "15")
    EMAIL_SECRET: str = os.environ.get("EMAIL_SECRET", "649fb93ef34e4fdf4187709c84d643dd61ce730d91856418fdcf563f895ea40f")
    EMAIL_USERNAME: str = os.environ.get("EMAIL_USERNAME", "admin@gmail.com")
    EMAIL_PASSWORD: str = os.environ.get("EMAIL_PASSWORD", "123456")
    EMAIL_PORT: int = os.environ.get("EMAIL_PORT", 465)
    EMAIL_SERVER: str = os.environ.get("EMAIL_SERVER", "smtp.gmail.com")
    EMAIL_FROM_NAME: str = os.environ.get("EMAIL_FROM_NAME", "EngQuizz")

    # ADMIN
    ADMIN_FULLNAME: str = os.environ.get("ADMIN_FULLNAME", "Admin")
    ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL", "admin@gmail.com")
    ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "123456")

    # WEBSOCKET
    WEBSOCKET_URL: str = f"ws://{APP_HOST}:{APP_PORT}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
