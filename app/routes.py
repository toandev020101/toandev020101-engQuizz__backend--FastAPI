from fastapi import FastAPI

from app.core import get_settings
from app.apis.endpoints import *

settings = get_settings()


def init_router(app: FastAPI):
    app.include_router(auth_router)