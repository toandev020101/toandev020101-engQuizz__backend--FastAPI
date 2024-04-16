from pydantic import BaseModel


class OTPBase(BaseModel):
    code: str
    limited: int


class OTPCreateSchema(OTPBase):
    user_id: int


class OTPUpdateSchema(OTPBase):
    pass


class OTPSchema(OTPBase):
    id: int
