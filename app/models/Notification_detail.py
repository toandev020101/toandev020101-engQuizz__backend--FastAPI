from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models import BaseModel


class NotificationDetail(BaseModel):
    __tablename__ = "notification_details"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    user = relationship("User", back_populates="notification_details", lazy="selectin")

    notification_id = Column(Integer, ForeignKey('notifications.id'), primary_key=True, index=True)
    notification = relationship("Notification", back_populates="notification_details", lazy="selectin")

    is_readed = Column(Boolean, nullable=False, default=False, server_default="false")
