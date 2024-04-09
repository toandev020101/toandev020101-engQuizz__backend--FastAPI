from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.user_schema import UserSchema
from app.schemas.exam_detail_schema import ExamDetailSchema


class ExamBase(BaseModel):
    user_id: int = None
    test_id: int = None


class ExamCreateSchema(ExamBase):
    pass


class ExamUpdateSchema(ExamBase):
    exam_time_at: datetime
    exam_time: int


class ExamSchema(ExamBase):
    id: int
    user: UserSchema
    exam_details: List[ExamDetailSchema]
