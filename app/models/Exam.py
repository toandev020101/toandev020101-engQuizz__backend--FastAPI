from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models import BaseModel


class Exam(BaseModel):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    exam_time_at = Column(DateTime(timezone=True), nullable=True)
    exam_time = Column(Integer, default=0, server_default="0", nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="exams", lazy="selectin")

    test_id = Column(Integer, ForeignKey("tests.id"))
    test = relationship("Test", back_populates="exams", lazy="selectin")

    result = relationship("Result", back_populates="exam", lazy="selectin", cascade="all, delete")
    exam_details = relationship("ExamDetail", back_populates="exam", lazy="selectin", cascade="all, delete")

    def dict(self):
        return super().to_dict()