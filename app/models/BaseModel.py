from typing import List, Dict, Any

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import RelationshipProperty
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
    def extra_relationships(model_name: str, model, relationship_un_selects: Dict[str, Any]):
        result = {}
        for column in model.__table__.columns:
            if (not relationship_un_selects or model_name not in relationship_un_selects or column.name
                    not in relationship_un_selects[model_name]):
                value = getattr(model, column.name)
                # Add http://localhost only if the field is specified and is a string containing "uploads"
                if isinstance(value, str) and 'uploads' in value:
                    value = settings.SERVER_URL + value
                result[column.name] = value
        return result

    def dict(self, un_selects: List[str] = None, relationship_un_selects: Dict[str, Any] = None,
             relationships: Dict[str, Any] = None):
        result = {}
        # Get the values of the columns
        for column in self.__table__.columns:
            if not un_selects or column.name not in un_selects:
                value = getattr(self, column.name)
                # Add http://localhost only if the field is specified and is a string containing "uploads"
                if isinstance(value, str) and 'uploads' in value:
                    value = settings.SERVER_URL + value
                result[column.name] = value

        # Take the value of relationships if appointed
        if relationships:
            for relationship_name, subfields in relationships.items():
                if hasattr(self, relationship_name):
                    value = getattr(self, relationship_name)
                    if value is not None:
                        if isinstance(value, list):
                            result[relationship_name] = [
                                item.dict(un_selects=relationship_un_selects.get(relationship_name),
                                          relationship_un_selects=relationship_un_selects.get(relationship_name),
                                          relationships=subfields) for item in value
                            ]
                        elif isinstance(value.property, RelationshipProperty):
                            result[relationship_name] = value.dict(
                                un_selects=relationship_un_selects.get(relationship_name),
                                relationship_un_selects=relationship_un_selects.get(relationship_name),
                                relationships=subfields
                            )
                        else:
                            value = getattr(self, relationship_name)
                            # Add http://localhost only if the field is specified and is a string containing "uploads"
                            if isinstance(value, str) and 'uploads' in value:
                                value = settings.SERVER_URL + value
                            result[relationship_name] = value

        return result
