from typing import Optional, List

from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Exam, Test, User, Result
from app.schemas import ExamSchema, ExamCreateSchema, \
    ExamUpdateSchema


class CRUDExam(CRUDBase[ExamSchema, ExamCreateSchema, ExamUpdateSchema]):
    async def find_all(self, session: AsyncSession) -> List[ExamSchema]:
        return await self.get_all(session)

    async def find_list_submit_by_user_id(self, user_id: int, session: AsyncSession) -> List[ExamSchema]:
        return await self.get_all(session, and_(Exam.user_id == user_id, Exam.is_submitted == True))

    async def find_list_by_user_id(self, user_id: int, session: AsyncSession) -> List[ExamSchema]:
        return await self.get_all(session, Exam.user_id == user_id)

    async def find_pagination(self, _limit: int, _page: int, search_term: str, score: str, correct_quantity: str,
                              session: AsyncSession):
        conditions = []

        if search_term:
            conditions.append(or_(Exam.test.has(Test.name.ilike(f"%{search_term}%")),
                                  Exam.user.has(User.fullname.ilike(f"%{search_term}%")),
                                  Exam.user.has(User.email.ilike(f"%{search_term}%"))))

        if score != 'all':
            filters = score.split('-')
            conditions.append(Exam.result.has(Result.score.between(int(filters[0]), int(filters[1]))))

        if correct_quantity != 'all':
            filters = correct_quantity.split('-')
            if len(filters) == 1:
                conditions.append(Exam.result.has(Result.correct_quantity >= int(filters[0])))
            else:
                conditions.append(Exam.result.has(Result.correct_quantity.between(int(filters[0]), int(filters[1]))))

        return await self.get_multi(session, offset=_page * _limit, limit=_limit, *conditions)

    async def find_one_by_id(self, id: int, session: AsyncSession) -> Optional[ExamSchema]:
        return await self.get(session, Exam.id == id)

    async def create_list(self, exams_data: List[ExamCreateSchema], session: AsyncSession):
        return await self.create_bulk(session, objs_in=exams_data)

    async def update_one(
            self, id: int, exam_data: ExamUpdateSchema, session: AsyncSession
    ) -> Optional[Exam]:
        exam = await self.get(session, id=id)

        if exam:
            await self.update(session, obj_in=exam_data, db_obj=exam)

        return exam

    async def delete_one(self, session: AsyncSession, id: int) -> Optional[ExamSchema]:
        exam = await self.get(session, id=id)

        if exam:
            await self.delete(session, Exam.id == id)
            return exam

        return None

    async def delete_list(self, session: AsyncSession, ids: List[int]) -> List[ExamSchema]:
        return await self.delete_bulk(session, ids=ids)


crud_exam = CRUDExam(Exam)
