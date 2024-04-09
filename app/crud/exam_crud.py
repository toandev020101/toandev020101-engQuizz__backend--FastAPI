from datetime import datetime
from typing import Optional, List

from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Exam
from app.schemas import ExamSchema, ExamCreateSchema, \
    ExamUpdateSchema


class CRUDExam(CRUDBase[ExamSchema, ExamCreateSchema, ExamUpdateSchema]):
    async def find_list_by_user_id(self, user_id: int, session: AsyncSession) -> List[ExamSchema]:
        return await self.get_all(session, Exam.user_id == user_id)

    # async def find_pagination(self, _limit: int, _page: int, search_term: str, status_exam: str, session: AsyncSession):
    #     conditions = []
    #
    #     if search_term:
    #         conditions.append(or_(Exam.content.ilike(f"%{search_term}%"),
    #                               Exam.answers.any(Answer.content.ilike(f"%{search_term}%"))))
    #
    #     if status_exam != 'all':
    #         current_date = datetime.now()
    #         if status_exam == "Chưa mở":
    #             conditions.append(Exam.start_date > current_date)
    #         elif status_exam == "Đang mở":
    #             conditions.append(and_(Exam.start_date <= current_date, current_date <= Exam.end_date))
    #         elif status_exam == "Đã đóng":
    #             conditions.append(Exam.end_date < current_date)
    #
    #     return await self.get_multi(session, offset=_page * _limit, limit=_limit, *conditions)

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
