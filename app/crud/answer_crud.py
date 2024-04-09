from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Answer
from app.schemas import AnswerSchema, AnswerCreateSchema, AnswerUpdateSchema


class CRUDAnswer(CRUDBase[AnswerSchema, AnswerCreateSchema, AnswerUpdateSchema]):
    async def find_one_by_id(self, id: int, session: AsyncSession) -> Optional[Answer]:
        return await self.get(session, Answer.id == id)

    async def create_list(self, question_id: int, answers_data: List[AnswerCreateSchema], session: AsyncSession):
        for answer in answers_data:
            answer.question_id = question_id
        return await self.create_bulk(session, objs_in=answers_data)

    async def delete_list_by_question_id(self, session: AsyncSession, question_id: int) -> List[AnswerSchema]:
        answers = await self.get_all(session, Answer.question_id == question_id)
        return await self.delete_bulk(session, db_objs=answers)


crud_answer = CRUDAnswer(Answer)
