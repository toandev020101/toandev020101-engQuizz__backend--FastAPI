from sqlalchemy import Column, String, Boolean, Integer, Enum, Date
from sqlalchemy.orm import relationship

from app.enums import GenderEnum
from app.models import BaseModel

gender_values = [member.value for member in GenderEnum.__members__.values()]


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=True)
    password = Column(String(65), nullable=False)
    gender = Column(Enum(*gender_values, name='gender'), default=GenderEnum.MALE.value,
                    server_default=GenderEnum.MALE.value, nullable=False)
    birth_day = Column(Date, nullable=False)
    avatar = Column(String, nullable=True)

    is_verified = Column(Boolean, default=False, server_default="false", nullable=False)
    is_admin = Column(Boolean, default=False, server_default="false", nullable=False)
    token_version = Column(Integer, default=0, server_default="0", nullable=False)

    otp = relationship("OTP", back_populates="user", uselist=False, lazy="selectin", cascade="all, delete")
    notifications = relationship("Notification", back_populates="creator", lazy="selectin", cascade="all, delete")
    notification_details = relationship("NotificationDetail", back_populates="user", lazy="selectin", cascade="all, delete")
    questions = relationship("Question", back_populates="creator", lazy="selectin", cascade="all, delete")
    exams = relationship("Exam", back_populates="user", lazy="selectin", cascade="all, delete")
    tests = relationship("Test", back_populates="creator", lazy="selectin", cascade="all, delete")

    def dict(self, un_selects=None):
        result = super().to_dict(un_selects=un_selects)
        result["otp"] = self.otp.to_dict() if self.otp is not None else None
        return result
