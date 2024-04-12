from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.crud import crud_exam_detail
from app.schemas import ExamDetailUpdateSchema

settings = get_settings()


class ExamDetailService:
    @staticmethod
    async def update_answer_id_by_id(exam_id: int, question_id: int, exam_detail_data: ExamDetailUpdateSchema,
                                     session: AsyncSession):
        await crud_exam_detail.update_one(exam_id=exam_id, question_id=question_id, exam_detail_data=exam_detail_data, session=session)
        await session.commit()
