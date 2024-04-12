from typing import Optional, List

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import ExamDetail
from app.schemas import ExamDetailSchema, ExamDetailCreateSchema, \
    ExamDetailUpdateSchema


class CRUDExamDetail(CRUDBase[ExamDetailSchema, ExamDetailCreateSchema, ExamDetailUpdateSchema]):
    async def create_list(self, exam_details_data: List[ExamDetailCreateSchema], session: AsyncSession):
        return await self.create_bulk(session, objs_in=exam_details_data)

    async def update_one(
            self, exam_id: int, question_id: int, exam_detail_data: ExamDetailUpdateSchema, session: AsyncSession
    ) -> Optional[ExamDetail]:
        exam_detail = await self.get(session, and_(ExamDetail.exam_id == exam_id, ExamDetail.question_id == question_id))

        if exam_detail:
            await self.update(session, obj_in=exam_detail_data, db_obj=exam_detail)

        return exam_detail


crud_exam_detail = CRUDExamDetail(ExamDetail)
