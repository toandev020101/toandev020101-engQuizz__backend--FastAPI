from typing import List

from pydantic import BaseModel


class NotificationDetailBase(BaseModel):
    user_id: int = None
    notification_id: int = None


class NotificationDetailCreateSchema(NotificationDetailBase):
    pass


class NotificationDetailUpdateSchema(NotificationDetailBase):
    is_readed: bool


class NotificationDetailSchema(NotificationDetailBase):
    id: int

