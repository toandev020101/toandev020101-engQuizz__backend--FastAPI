from datetime import date

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    fullname: str
    email: EmailStr
    gender: str
    birth_day: date


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchema(UserBase):
    avatar: str = None
    password: str


class UserUpdateSchema(UserBase):
    avatar: str = None
    is_admin: bool


class UserChangeIsAdminSchema(BaseModel):
    is_admin: bool


class UserSchema(UserBase):
    id: int
    avatar: str
    is_verified: bool
    is_admin: bool
    token_version: int
