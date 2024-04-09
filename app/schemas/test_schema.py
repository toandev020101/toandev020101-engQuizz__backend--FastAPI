from datetime import datetime
from typing import Any, List

from pydantic import BaseModel

from app.schemas.exam_schema import ExamSchema


class TestBase(BaseModel):
    name: str
    start_date: str
    end_date: str
    exam_time: int
    easy_quantity: int
    average_quantity: int
    difficult_quantity: int
    mix_question: bool
    mix_answer: bool
    show_exam: bool
    show_result: bool
    show_answer: bool


class TestCreateSchema(TestBase):
    exams: Any
    creator_id: int = None


class TestUpdateSchema(TestBase):
    exams: Any


class TestSchema(TestBase):
    id: int
    exams: List[ExamSchema]
