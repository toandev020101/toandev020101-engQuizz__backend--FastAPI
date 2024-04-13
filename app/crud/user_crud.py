from typing import Optional, List

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import User
from app.schemas import UserSchema, UserUpdateSchema, UserCreateSchema


class CRUDUser(CRUDBase[UserSchema, UserCreateSchema, UserUpdateSchema]):
    async def find_pagination(self, _limit: int, _page: int, search_term: str, gender: str,
                              is_admin: str, session: AsyncSession):
        conditions = []

        if search_term:
            conditions.append(or_(User.fullname.ilike(f"%{search_term}%"), User.email.ilike(f"%{search_term}%")))

        if gender != 'all':
            conditions.append(User.gender == gender)

        if is_admin != 'all':
            bool_value = is_admin.lower() == "true"
            conditions.append(User.is_admin == bool_value)

        return await self.get_multi(session, offset=_page * _limit, limit=_limit, *conditions)

    async def find_list_by_role(self, session: AsyncSession) -> List[UserSchema]:
        return await self.get_all(session, User.is_admin == False)

    async def find_one_by_id(self, id: int, session: AsyncSession) -> Optional[UserSchema]:
        return await self.get(session, User.id == id)

    async def find_one_by_email(self, email: str, session: AsyncSession) -> Optional[UserSchema]:
        return await self.get(session, User.email == email)

    async def create_one(self, user_data: UserCreateSchema, session: AsyncSession):
        return await self.create(session, obj_in=user_data)

    async def update_one(
            self, id: int, user_data: UserUpdateSchema, session: AsyncSession
    ) -> Optional[User]:
        user = await self.get(session, id=id)

        if user:
            await self.update(session, obj_in=user_data, db_obj=user)

        return user

    async def update_token_version(
            self, id: int, token_version: int, session: AsyncSession
    ) -> Optional[User]:
        user = await self.get(session, id=id)

        if user:
            update_data = {"token_version": token_version}
            await self.update(session, obj_in=update_data, db_obj=user)

        return user

    async def verify_email(
            self, id: int, session: AsyncSession
    ) -> Optional[User]:
        user = await self.get(session, id=id)

        if user:
            update_data = {"is_verified": True}
            await self.update(session, obj_in=update_data, db_obj=user)

        return user

    async def change_is_admin(
            self, id: int, is_admin: bool, session: AsyncSession
    ) -> Optional[User]:
        user = await self.get(session, id=id)

        if user:
            update_data = {"is_admin": is_admin}
            await self.update(session, obj_in=update_data, db_obj=user)

        return user

    async def change_password(
            self, id: int, new_password: str, session: AsyncSession
    ) -> Optional[User]:
        user = await self.get(session, id=id)

        if user:
            user.password = new_password
            await session.commit()

        return user

    async def delete_one(self, session: AsyncSession, id: int) -> Optional[UserSchema]:
        user = await self.get(session, id=id)

        if user:
            await self.delete(session, User.id == id)
            return user

        return None

    async def delete_list(self, session: AsyncSession, ids: List[int]) -> List[UserSchema]:
        return await self.delete_bulk(session, ids=ids)


crud_user = CRUDUser(User)
