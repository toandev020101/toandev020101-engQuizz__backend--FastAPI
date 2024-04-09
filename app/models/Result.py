from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models import BaseModel


class Result(BaseModel):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, default=0, server_default="0", nullable=False)
    correct_quantity = Column(Integer, default=0, server_default="0", nullable=False)

    exam_id = Column(Integer, ForeignKey('exams.id'))
    exam = relationship("Exam", back_populates="result", uselist=False, lazy="selectin", cascade="all, delete")

    def dict(self):
        return super().to_dict()
