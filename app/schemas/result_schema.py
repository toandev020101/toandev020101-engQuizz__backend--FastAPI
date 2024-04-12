from pydantic import BaseModel


class ResultBase(BaseModel):
    score: float
    correct_quantity: int


class ResultCreateSchema(ResultBase):
    exam_id: int


class ResultUpdateSchema(ResultBase):
    pass


class ResultSchema(ResultBase):
    id: int
