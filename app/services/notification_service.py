from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.crud import crud_notification, crud_notification_detail
from app.schemas import NotificationCreateSchema, NotificationDetailCreateSchema
from app.utils import to_list_dict

settings = get_settings()


class NotificationService:
    @staticmethod
    async def get_pagination(_limit: int, _page: int, search_term: str, session: AsyncSession):
        notifications = await crud_notification.find_pagination(_limit=_limit, _page=_page, search_term=search_term,
                                                                session=session)

        total = await crud_notification.count_all(session=session)
        return {"notifications": to_list_dict(objects=notifications), "total": total}

    @staticmethod
    async def get_list_by_user_id(user_id: int, session: AsyncSession):
        notifications = await crud_notification.find_list_by_user_id(user_id=user_id, session=session)
        return {"notifications": to_list_dict(objects=notifications)}

    @staticmethod
    async def read_all(user_id: int, session: AsyncSession):
        await crud_notification_detail.read_all(user_id=user_id, session=session)

    @staticmethod
    async def add_one(creator_id: int, notification_data: NotificationCreateSchema, type_message: str,
                      session: AsyncSession):
        notification_user_ids = notification_data.user_ids
        del notification_data.user_ids
        notification_data.creator_id = creator_id
        created_notification = await crud_notification.create_one(notification_data=notification_data, session=session)
        notification_details_data = []
        for notification_user_id in notification_user_ids:
            notification_details_data.append(NotificationDetailCreateSchema(
                user_id=notification_user_id,
                notification_id=created_notification.id
            ))

        await crud_notification_detail.create_list(notification_details_data=notification_details_data,
                                                   session=session)

        await crud_notification.send_message(user_ids=notification_user_ids, type=type_message,
                                             text=created_notification.title)
        return {"notification": created_notification.dict()}

    @staticmethod
    async def remove_one(id: int, session: AsyncSession):
        removed_notification = await crud_notification.delete_one(id=id, session=session)
        if not removed_notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy thông báo!")
        return removed_notification.dict()

    @staticmethod
    async def remove_list(ids: List[int], session: AsyncSession):
        removed_notifications = await crud_notification.delete_list(ids=ids, session=session)
        if not removed_notifications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy thông báo!")
        return to_list_dict(objects=removed_notifications)
