from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import NotificationDetail
from app.schemas import NotificationDetailSchema, NotificationDetailCreateSchema, \
    NotificationDetailUpdateSchema


class CRUDNotificationDetail(
    CRUDBase[NotificationDetailSchema, NotificationDetailCreateSchema, NotificationDetailUpdateSchema]):
    async def create_list(self, notification_details_data: List[NotificationDetailCreateSchema], session: AsyncSession):
        return await self.create_bulk(session, objs_in=notification_details_data)

    async def read_all(
            self, user_id: int,
            session: AsyncSession
    ):
        notification_details = await self.get_all(session, NotificationDetail.user_id == user_id)
        notification_details_data = []
        for notification_detail in notification_details:
            notification_detail_data = NotificationDetailUpdateSchema(is_readed=True)
            notification_details_data.append(notification_detail_data)

        if len(notification_details) > 0:
            await self.update_bulk(session, objs_in=notification_details_data, db_objs=notification_details)


crud_notification_detail = CRUDNotificationDetail(NotificationDetail)
