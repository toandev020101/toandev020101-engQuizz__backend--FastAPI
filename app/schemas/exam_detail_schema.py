from datetime import datetime

from pydantic import BaseModel

from app.schemas.answer_schema import AnswerSchema
from app.schemas.question_schema import QuestionSchema


class ExamDetailBase(BaseModel):
    position: int = None
    exam_id: int = None
    question_id: int = None


class ExamDetailCreateSchema(ExamDetailBase):
    pass


class ExamDetailUpdateSchema(ExamDetailBase):
    answer_id: int


class ExamDetailSchema(ExamDetailBase):
    id: int
    answer: AnswerSchema
    question: QuestionSchema
