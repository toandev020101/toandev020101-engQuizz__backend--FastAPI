from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.enums import LevelEnum
from app.models import BaseModel

level_values = [member.value for member in LevelEnum.__members__.values()]


class Question(BaseModel):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(300), unique=True, nullable=False)
    level = Column(Enum(*level_values, name='level'), nullable=False)

    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="questions", lazy="selectin")

    answers = relationship("Answer", back_populates="question", lazy="selectin", cascade="all, delete")
    exam_details = relationship("ExamDetail", back_populates="question", lazy="selectin", cascade="all, delete")
