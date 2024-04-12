from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models import BaseModel


class ExamDetail(BaseModel):
    __tablename__ = "exam_details"

    exam_id = Column(Integer, ForeignKey('exams.id'), primary_key=True, index=True)
    exam = relationship("Exam", back_populates="exam_details", lazy="selectin")

    answer_id = Column(Integer, ForeignKey('answers.id'), index=True, nullable=True)
    answer = relationship("Answer", back_populates="exam_details", lazy="selectin")

    question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True, index=True)
    question = relationship("Question", back_populates="exam_details", lazy="selectin")

    position = Column(Integer, default=0, server_default="0", nullable=False)
    is_answer_draft = Column(Boolean, default=False, server_default="false", nullable=False)

    def dict(self):
        return super().to_dict()
