from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models import BaseModel


class OTP(BaseModel):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(6), nullable=False)
    limited = Column(Integer, default=5, server_default="5", nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="otp", uselist=False, lazy="selectin")

    def dict(self, un_selects=None):
        return super().to_dict()
