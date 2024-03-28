from app.core import SessionLocal


async def get_session():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
