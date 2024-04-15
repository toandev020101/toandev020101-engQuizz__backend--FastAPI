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
        result = super().to_dict()
        result["notification_details"] = []
        for notification_detail in self.notification_details:
            result["notification_details"].append({
                **notification_detail.to_dict(),
                "user": notification_detail.user.dict(un_selects=["password"])
            })
        return result
