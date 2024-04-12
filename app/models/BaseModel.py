from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

from app.core import Base, get_settings

settings = get_settings()


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), server_default=func.now(),
                         server_onupdate=func.now(),
                         nullable=False)

    def to_dict(self, un_selects=None):
        result = {}
        for column in self.__table__.columns:
            if not un_selects or column.name not in un_selects:
                result[column.name] = getattr(self, column.name)
        return result
