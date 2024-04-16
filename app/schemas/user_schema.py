from datetime import date

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    fullname: str
    email: EmailStr = None
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
    is_admin: bool = None


class UserChangeIsAdminSchema(BaseModel):
    is_admin: bool


class UserChangePasswordSchema(BaseModel):
    password: str
    new_password: str
    confirm_new_password: str


class UserSchema(UserBase):
    id: int
    avatar: str
    is_verified: bool
    is_admin: bool
    token_version: int


class UserForgotPasswordSchema(BaseModel):
    email: str
    new_password: str
    otp: str


class UserOTPPasswordSchema(BaseModel):
    otp: str
    email: str


class UserSendOTPPasswordSchema(BaseModel):
    email: str


class UserRefreshOTPSchema(BaseModel):
    email: str
