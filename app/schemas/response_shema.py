from typing import Optional, TypeVar, Dict
from pydantic import BaseModel

T = TypeVar('T')


class ResponseSchema(BaseModel):
    status_code: int
    detail: str
    data: Optional[T] = None
