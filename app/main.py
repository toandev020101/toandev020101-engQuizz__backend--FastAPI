import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.core import get_settings, Base, engine
from app.middlewares import logging_middleware
from app.routes import init_router

settings = get_settings()
origins = [settings.CLIENT_URL]


def init_app():
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION
    )

    app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    init_router(app)

    return app


root = init_app()


def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run(app="app.main:root", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
