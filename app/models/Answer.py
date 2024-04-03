from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models import BaseModel


class Answer(BaseModel):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(300), unique=True, nullable=False)
    is_correct = Column(Boolean, default=False, server_default="false", nullable=False)

    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship("Question", back_populates="answers", lazy="selectin")
