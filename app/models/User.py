from enum import Enum as PythonEnum

from sqlalchemy import Column, String, Boolean, Integer, Enum, Date

from app.models import BaseModel


class Gender(PythonEnum):
    MALE = "Nam"
    FEMALE = "Nữ"


gender_values = [member.value for member in Gender.__members__.values()]


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=True)
    password = Column(String(65), nullable=False)
    gender = Column(Enum(*gender_values, name='gender'), default=Gender.MALE.value,
                    server_default=Gender.MALE.value, nullable=False)
    birth_day = Column(Date, nullable=False)
    avatar = Column(String, nullable=True)

    is_verified = Column(Boolean, default=False, server_default="false", nullable=False)
    is_admin = Column(Boolean, default=False, server_default="false", nullable=False)
    token_version = Column(Integer, default=0, server_default="0", nullable=False)
