from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends import get_session, check_auth
from app.core import get_settings
from app.schemas import ResponseSchema, RemoveSchema, NotificationCreateSchema
from app.services import NotificationService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/notification", tags=["Notification"])


@router.get("/pagination", response_model=ResponseSchema)
async def get_notification_pagination(_limit: int = 5, _page: int = 0, search_term: str = "",
                                      session: AsyncSession = Depends(get_session),
                                      user_decode=Depends(check_auth)):
    data = await NotificationService.get_pagination(_limit=_limit, _page=_page, search_term=search_term,
                                                    session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách thông báo thành công", data=data)


@router.get("", response_model=ResponseSchema)
async def get_notification_list_by_user_id(session: AsyncSession = Depends(get_session),
                                           user_decode=Depends(check_auth)):
    data = await NotificationService.get_list_by_user_id(user_id=user_decode.get("user_id"), session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách thông báo thành công", data=data)


@router.get("/read-all", response_model=ResponseSchema)
async def read_all_notification(session: AsyncSession = Depends(get_session),
                                user_decode=Depends(check_auth)):
    await NotificationService.read_all(user_id=user_decode.get("user_id"), session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Đọc tất cả thông báo thành công")


@router.post("", response_model=ResponseSchema)
async def add_notification_one(notification_data: NotificationCreateSchema,
                               session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    await NotificationService.add_one(creator_id=user_decode.get("user_id"), notification_data=notification_data,
                                      type_message="info", session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thêm thông báo thành công")


@router.delete("/{id}", response_model=ResponseSchema)
async def remove_notification_one(id: int, session: AsyncSession = Depends(get_session),
                                  user_decode=Depends(check_auth)):
    data = await NotificationService.remove_one(id=id, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa thông báo thành công", data=data)


@router.delete("", response_model=ResponseSchema)
async def remove_notification_list(remove_data: RemoveSchema, session: AsyncSession = Depends(get_session),
                                   user_decode=Depends(check_auth)):
    data = await NotificationService.remove_list(ids=remove_data.ids, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa danh sách thông báo thành công", data=data)
