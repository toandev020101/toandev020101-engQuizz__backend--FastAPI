from typing import List, Dict

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

    @staticmethod
    def extra_relationships(model_name: str, model, relationship_levels: Dict[str, bool], current_level: int = 1):
        result = {}
        if current_level <= 0:
            return None

        for column in model.__table__.columns:
            result[column.name] = getattr(model, column.name)

        for relationship_name in model.__mapper__.relationships.keys():
            if relationship_levels.get(relationship_name, False):
                value = getattr(model, relationship_name)
                if value is not None:
                    if isinstance(value, list):
                        result[relationship_name] = [
                            BaseModel.extra_relationships(
                                model_name=relationship_name,
                                model=item,
                                relationship_levels=relationship_levels,
                                current_level=current_level - 1
                            ) for item in value
                        ]
                    else:
                        result[relationship_name] = BaseModel.extra_relationships(
                            model_name=relationship_name,
                            model=value,
                            relationship_levels=relationship_levels,
                            current_level=current_level - 1
                        )

        return result

    def dict(self, un_selects: List[str] = None, relationship_levels: Dict[str, bool] = None):
        result = {}
        for column in self.__table__.columns:
            if not un_selects or column.name not in un_selects:
                result[column.name] = getattr(self, column.name)

        if relationship_levels:
            for relationship_name, include in relationship_levels.items():
                if include and hasattr(self, relationship_name):
                    value = getattr(self, relationship_name)
                    if value is not None:
                        if isinstance(value, list):
                            result[relationship_name] = [
                                BaseModel.extra_relationships(
                                    model_name=relationship_name,
                                    model=item,
                                    relationship_levels=relationship_levels,
                                    current_level=1
                                ) for item in value
                            ]
                        else:
                            result[relationship_name] = BaseModel.extra_relationships(
                                model_name=relationship_name,
                                model=value,
                                relationship_levels=relationship_levels,
                                current_level=1
                            )

        return result

