from typing import List

from pydantic import BaseModel

from app.schemas.notification_detail_schema import NotificationDetailSchema


class NotificationBase(BaseModel):
    title: str
    content: str


class NotificationCreateSchema(NotificationBase):
    creator_id: int = None
    user_ids: List[int]


class NotificationUpdateSchema(NotificationBase):
    user_ids: List[int]


class NotificationSchema(NotificationBase):
    id: int
    notification_details: List[NotificationDetailSchema]