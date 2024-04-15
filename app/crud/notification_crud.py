import json
from typing import Optional, List

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.endpoints.websocket_endpoint import notification_users
from app.crud import CRUDBase
from app.models import Notification, NotificationDetail
from app.schemas import NotificationSchema, NotificationCreateSchema, \
    NotificationUpdateSchema


class CRUDNotification(CRUDBase[NotificationSchema, NotificationCreateSchema, NotificationUpdateSchema]):
    async def find_list_by_user_id(self, user_id: int, session: AsyncSession) -> List[NotificationSchema]:
        return await self.get_all(session, Notification.notification_details.any(NotificationDetail.user_id == user_id))

    async def find_pagination(self, _limit: int, _page: int, search_term: str, session: AsyncSession):
        conditions = []

        if search_term:
            conditions.append(
                or_(Notification.title.ilike(f"%{search_term}%"), Notification.content.ilike(f"%{search_term}%")))

        return await self.get_multi(session, offset=_page * _limit, limit=_limit, *conditions)

    async def find_one_by_id(self, id: int, session: AsyncSession) -> Optional[NotificationSchema]:
        return await self.get(session, Notification.id == id)

    async def create_one(self, notification_data: NotificationCreateSchema, session: AsyncSession):
        return await self.create(session, obj_in=notification_data)

    async def delete_one(self, session: AsyncSession, id: int) -> Optional[NotificationSchema]:
        notification = await self.get(session, id=id)

        if notification:
            await self.delete(session, Notification.id == id)
            return notification

        return None

    async def delete_list(self, session: AsyncSession, ids: List[int]) -> List[NotificationSchema]:
        return await self.delete_bulk(session, ids=ids)

    @staticmethod
    async def send_message(user_ids: List[int], type: str, text: str):
        message = {"type": type, "text": text}
        for notification_user in notification_users:
            if notification_user["user_id"] in user_ids:
                await notification_user["websocket"].send_text(json.dumps(message))


crud_notification = CRUDNotification(Notification)
