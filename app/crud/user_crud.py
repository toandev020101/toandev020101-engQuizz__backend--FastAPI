from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.crud import CRUDBase
from app.schemas import UserSchema, UserUpdateSchema, UserCreateSchema


class CRUDUser(CRUDBase[UserSchema, UserCreateSchema, UserUpdateSchema]):
    async def find_one_by_id(self, id: int, session: AsyncSession) -> Optional[User]:
        return await self.get(session, User.id == id)

    async def find_one_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        return await self.get(session, User.email == email)

    async def create_one(self, schema: UserCreateSchema, session: AsyncSession):
        return await self.create(session=session, obj_in=schema)

    async def update_token_version(
        self, user_id: int, token_version: int, session: AsyncSession
    ) -> Optional[User]:
        user = await self.get(session, id=user_id)

        if user:
            update_data = {"token_version": token_version}
            await self.update(session, obj_in=update_data, db_obj=user)

        return user


crud_user = CRUDUser(User)