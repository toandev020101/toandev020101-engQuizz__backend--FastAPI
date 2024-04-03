from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from app.models import BaseModel


class Test(BaseModel):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    exam_time = Column(Integer, default=0, server_default="0", nullable=False)

    easy_quantity = Column(Integer, default=0, server_default="0", nullable=False)
    average_quantity = Column(Integer, default=0, server_default="0", nullable=False)
    difficult_quantity = Column(Integer, default=0, server_default="0", nullable=False)

    mix_question = Column(Boolean, default=False, server_default="false", nullable=False)
    mix_answer = Column(Boolean, default=False, server_default="false", nullable=False)
    show_exam = Column(Boolean, default=False, server_default="false", nullable=False)
    show_result = Column(Boolean, default=False, server_default="false", nullable=False)
    show_answer = Column(Boolean, default=False, server_default="false", nullable=False)

    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="tests", lazy="selectin")

    exams = relationship("Exam", back_populates="test", lazy="selectin", cascade="all, delete")
