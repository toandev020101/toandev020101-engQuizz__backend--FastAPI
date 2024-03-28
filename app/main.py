import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app.apis.endpoints import *
from app.core import get_settings
from app.middlewares import logging_middleware

settings = get_settings()


def init_app():
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION
    )

    app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
    app.include_router(auth_router)

    return app


root = init_app()


def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run(app="app.main:root", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
