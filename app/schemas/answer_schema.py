from pydantic import BaseModel


class AnswerBase(BaseModel):
    content: str
    is_correct: bool
    question_id: int = None


class AnswerCreateSchema(AnswerBase):
    pass


class AnswerUpdateSchema(AnswerBase):
    pass


class AnswerSchema(AnswerBase):
    id: int
