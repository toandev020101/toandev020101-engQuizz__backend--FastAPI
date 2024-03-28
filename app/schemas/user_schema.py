from datetime import date

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    gender: str
    birth_day: date


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchema(UserBase):
    pass


class UserUpdateSchema(UserBase):
    id: int
    avatar: str
    is_verified: bool
    is_admin: bool


class UserSchema(UserBase):
    id: int
    avatar: str
    is_verified: bool
    is_admin: bool
    token_version: int
