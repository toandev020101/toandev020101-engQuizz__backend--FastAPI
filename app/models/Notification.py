from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models import BaseModel


class Notification(BaseModel):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="notifications", lazy="selectin")

    notification_details = relationship("NotificationDetail", back_populates="notification", lazy="selectin",
                                        cascade="all, delete")

    def dict(self, un_selects=None):
        return super().to_dict()