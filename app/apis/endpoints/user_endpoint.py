from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends import get_session, check_auth
from app.core import get_settings
from app.schemas import ResponseSchema, RemoveSchema, UserChangeIsAdminSchema, UserCreateSchema, UserUpdateSchema, \
    UserChangePasswordSchema
from app.services import UserService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/user", tags=["User"])


@router.get("", response_model=ResponseSchema)
async def get_user_pagination(_limit: int = 5, _page: int = 0, search_term: str = "", gender: str = "all",
                              is_admin: str = "all", session: AsyncSession = Depends(get_session),
                              user_decode=Depends(check_auth)):
    data = await UserService.get_pagination(_limit=_limit, _page=_page, search_term=search_term, gender=gender,
                                            is_admin=is_admin, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách tài khoản thành công", data=data)


@router.get("/any/student", response_model=ResponseSchema)
async def get_list_user_by_role(session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    data = await UserService.get_list_by_role(session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách tài khoản thành công", data=data)


@router.get("/{id}", response_model=ResponseSchema)
async def get_user_one_by_id(id: int, session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    data = await UserService.get_one_by_id(id=id, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy thông tin tài khoản thành công", data=data)


@router.post("", response_model=ResponseSchema)
async def add_user_one(user_data: UserCreateSchema,
                       session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    await UserService.add_one(user_data=user_data, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thêm tài khoản thành công")


@router.put("/{id}", response_model=ResponseSchema)
async def update_user_one(id: int, user_data: UserUpdateSchema,
                          session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    await UserService.update_one(id=id, user_data=user_data, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Cập nhật tài khoản thành công")


@router.patch("/{id}", response_model=ResponseSchema)
async def change_user_is_admin(id: int, user_data: UserChangeIsAdminSchema,
                               session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    await UserService.change_is_admin(id=id, is_admin=user_data.is_admin, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thay đổi vai trò thành công")


@router.patch("", response_model=ResponseSchema)
async def change_user_password(user_data: UserChangePasswordSchema,
                               session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    await UserService.change_password(id=user_decode.get("user_id"), user_data=user_data, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thay đổi mật khẩu thành công")


@router.delete("/{id}", response_model=ResponseSchema)
async def remove_user_one(id: int, session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    data = await UserService.remove_one(id=id, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa tài khoản thành công", data=data)


@router.delete("", response_model=ResponseSchema)
async def remove_user_list(remove_data: RemoveSchema, session: AsyncSession = Depends(get_session),
                           user_decode=Depends(check_auth)):
    data = await UserService.remove_list(ids=remove_data.ids, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa danh sách tài khoản thành công", data=data)
