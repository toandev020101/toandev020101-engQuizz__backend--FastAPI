from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.crud import crud_exam, crud_result
from app.schemas import ExamUpdateSchema, ResultCreateSchema
from app.utils import to_list_dict

settings = get_settings()


class ExamService:
    @staticmethod
    async def get_list_by_user_id(user_id: int, session: AsyncSession):
        exams = await crud_exam.find_list_by_user_id(user_id=user_id, session=session)
        return {"exams": to_list_dict(objects=exams)}

    @staticmethod
    async def get_one_by_id(id: int, session: AsyncSession):
        exam = await crud_exam.find_one_by_id(id=id, session=session)
        return {"exam": exam.dict()}

    @staticmethod
    async def update_exam_time_by_id(id: int, exam_data: ExamUpdateSchema, session: AsyncSession):
        await crud_exam.update_one(id=id, exam_data=exam_data, session=session)
        await session.commit()

    @staticmethod
    async def submit_exam(id: int, session: AsyncSession):
        exam = await crud_exam.find_one_by_id(id=id, session=session)
        if exam is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy đề thi!")

        correct_quantity = 0
        for exam_detail in exam.exam_details:
            for answer in exam_detail.question.answers:
                if answer.is_correct:
                    if exam_detail.answer_id == answer.id:
                        correct_quantity += 1
        score = correct_quantity / len(exam.exam_details) * 10

        result_data = ResultCreateSchema(score=score, correct_quantity=correct_quantity, exam_id=exam.id)
        await crud_result.create_one(result_data=result_data, session=session)
        updated_exam = await crud_exam.update_one(id=exam.id, exam_data=ExamUpdateSchema(is_submitted=True), session=session)
        await session.commit()

        return updated_exam
