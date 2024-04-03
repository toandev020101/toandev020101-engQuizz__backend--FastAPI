from typing import List

from pydantic import BaseModel

from app.schemas import AnswerSchema, AnswerUpdateSchema, AnswerCreateSchema


class QuestionBase(BaseModel):
    content: str
    level: str


class QuestionCreateSchema(QuestionBase):
    answers: List[AnswerCreateSchema]
    creator_id: int = None


class QuestionUpdateSchema(QuestionBase):
    answers: List[AnswerUpdateSchema]


class QuestionSchema(QuestionBase):
    id: int
    answers: List[AnswerSchema]
