from typing import Optional, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class ResponseSchema(BaseModel):
    code: int
    message: str
    data: Optional[T] = None
