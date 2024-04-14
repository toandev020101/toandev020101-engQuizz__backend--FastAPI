from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models import BaseModel


class Exam(BaseModel):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    exam_time_at = Column(DateTime(timezone=True), nullable=True)
    exam_time = Column(Integer, default=0, server_default="0", nullable=True)
    is_submitted = Column(Boolean, default=False, server_default="false", nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="exams", lazy="selectin")

    test_id = Column(Integer, ForeignKey("tests.id"))
    test = relationship("Test", back_populates="exams", lazy="selectin")

    result = relationship("Result", back_populates="exam", uselist=False, lazy="selectin", cascade="all, delete")
    exam_details = relationship("ExamDetail", back_populates="exam", lazy="selectin", cascade="all, delete")

    def dict(self, un_selects=None):
        result = super().to_dict()
        result["test"] = self.test.to_dict()
        result["user"] = self.user.to_dict(un_selects=["password"])
        result["exam_details"] = []
        if self.result:
            result["result"] = self.result.to_dict()
        for exam_detail in self.exam_details:
            question = {
                **exam_detail.question.to_dict(),
                "answers": [answer.to_dict(un_selects=un_selects) for answer in exam_detail.question.answers],
            }

            result["exam_details"].append({
                **exam_detail.to_dict(),
                "question": question
            })
        return result
