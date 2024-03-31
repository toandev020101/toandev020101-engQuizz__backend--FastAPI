from app.core import SessionLocal


async def get_session():
    session = SessionLocal()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e  # Raise the exception again to allow FastAPI to handle it
    finally:
        await session.close()

