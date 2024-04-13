from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.crud import crud_user
from app.schemas import UserCreateSchema, UserUpdateSchema, UserChangePasswordSchema
from app.utils import to_list_dict, hash_password, verify_password

settings = get_settings()


class UserService:
    @staticmethod
    async def get_pagination(_limit: int, _page: int, search_term: str, gender: str, is_admin: str,
                             session: AsyncSession):
        users = await crud_user.find_pagination(_limit=_limit, _page=_page, search_term=search_term, gender=gender,
                                                is_admin=is_admin, session=session)

        total = await crud_user.count_all(session=session)
        return {"users": to_list_dict(objects=users), "total": total}

    @staticmethod
    async def get_list_by_role(session: AsyncSession):
        users = await crud_user.find_list_by_role(session=session)

        return {"users": to_list_dict(objects=users)}

    @staticmethod
    async def get_one_by_id(id: int, session: AsyncSession):
        user = await crud_user.find_one_by_id(id=id, session=session)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản!")

        return {"user": user.dict()}

    @staticmethod
    async def add_one(user_data: UserCreateSchema, session: AsyncSession):
        user = await crud_user.find_one_by_email(email=user_data.email, session=session)

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email đã tồn tại!")

        user_data.password = hash_password(user_data.password)
        created_user = await crud_user.create_one(user_data=user_data, session=session)
        return {"user": created_user.dict()}

    @staticmethod
    async def update_one(id: int, user_data: UserUpdateSchema, session: AsyncSession):
        user = await crud_user.find_one_by_id(id=id, session=session)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Không tìm thấy tài khoản!")

        updated_user = await crud_user.update_one(id=id, user_data=user_data, session=session)
        return {"user": updated_user.dict()}

    @staticmethod
    async def change_is_admin(id: int, is_admin: bool, session: AsyncSession):
        user = await crud_user.find_one_by_id(id=id, session=session)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản!")

        await crud_user.change_is_admin(id=id, is_admin=is_admin, session=session)

    @staticmethod
    async def change_password(id: int, user_data: UserChangePasswordSchema, session: AsyncSession):
        user = await crud_user.find_one_by_id(id=id, session=session)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản!")

        if not verify_password(user_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mật khẩu cũ không chính xác!")

        await crud_user.change_password(id=id, new_password=hash_password(user_data.new_password), session=session)

    @staticmethod
    async def remove_one(id: int, session: AsyncSession):
        removed_user = await crud_user.delete_one(id=id, session=session)
        if not removed_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy tài khoản!")
        return removed_user.dict()

    @staticmethod
    async def remove_list(ids: List[int], session: AsyncSession):
        removed_users = await crud_user.delete_list(ids=ids, session=session)
        if not removed_users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy tài khoản!")
        return to_list_dict(objects=removed_users)
