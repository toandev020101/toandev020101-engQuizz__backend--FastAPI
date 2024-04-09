from datetime import datetime
from typing import Optional, List

from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Test
from app.schemas import TestSchema, TestCreateSchema, \
    TestUpdateSchema


class CRUDTest(CRUDBase[TestSchema, TestCreateSchema, TestUpdateSchema]):
    async def find_pagination(self, _limit: int, _page: int, search_term: str, status_test: str, session: AsyncSession):
        conditions = []

        if search_term:
            conditions.append(Test.name.ilike(f"%{search_term}%"))

        if status_test != 'all':
            current_date = datetime.now()
            if status_test == "Chưa mở":
                conditions.append(Test.start_date > current_date)
            elif status_test == "Đang mở":
                conditions.append(and_(Test.start_date <= current_date, current_date <= Test.end_date))
            elif status_test == "Đã đóng":
                conditions.append(Test.end_date < current_date)

        return await self.get_multi(session, offset=_page * _limit, limit=_limit, *conditions)

    async def find_one_by_id(self, id: int, session: AsyncSession) -> Optional[TestSchema]:
        return await self.get(session, Test.id == id)

    async def create_one(self, test_data: TestCreateSchema, session: AsyncSession):
        return await self.create(session, obj_in=test_data)

    async def update_one(
        self, id: int, test_data: TestUpdateSchema, session: AsyncSession
    ) -> Optional[Test]:
        test = await self.get(session, id=id)

        if test:
            await self.update(session, obj_in=test_data, db_obj=test)

        return test

    async def delete_one(self, session: AsyncSession, id: int) -> Optional[TestSchema]:
        test = await self.get(session, id=id)

        if test:
            await self.delete(session, Test.id == id)
            return test

        return None

    async def delete_list(self, session: AsyncSession, ids: List[int]) -> List[TestSchema]:
        return await self.delete_bulk(session, ids=ids)


crud_test = CRUDTest(Test)
