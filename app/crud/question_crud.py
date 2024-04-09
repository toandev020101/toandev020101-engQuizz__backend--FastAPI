from typing import Optional, List

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Question, Answer
from app.schemas import QuestionSchema, QuestionCreateSchema, \
    QuestionUpdateSchema


class CRUDQuestion(CRUDBase[QuestionSchema, QuestionCreateSchema, QuestionUpdateSchema]):
    async def find_all(self, session: AsyncSession):
        return await self.get_all(session)

    async def find_pagination(self, _limit: int, _page: int, search_term: str, level: str, session: AsyncSession):
        conditions = []

        if search_term:
            conditions.append(or_(Question.content.ilike(f"%{search_term}%"),
                                  Question.answers.any(Answer.content.ilike(f"%{search_term}%"))))

        if level != 'all':
            conditions.append(Question.level == level)

        return await self.get_multi(session, offset=_page * _limit, limit=_limit, *conditions)

    async def find_one_by_id(self, id: int, session: AsyncSession) -> Optional[Question]:
        return await self.get(session, Question.id == id)

    async def find_one_by_content(self, content: str, session: AsyncSession) -> Optional[QuestionSchema]:
        return await self.get(session, Question.content == content)

    async def create_one(self, question_data: QuestionCreateSchema, session: AsyncSession):
        return await self.create(session, obj_in=question_data)

    async def update_one(
        self, id: int, question_data: QuestionUpdateSchema, session: AsyncSession
    ) -> Optional[Question]:
        question = await self.get(session, id=id)

        if question:
            await self.update(session, obj_in=question_data, db_obj=question)

        return question

    async def delete_one(self, session: AsyncSession, id: int) -> Optional[QuestionSchema]:
        question = await self.get(session, id=id)

        if question:
            await self.delete(session, Question.id == id)
            return question

        return None

    async def delete_list(self, session: AsyncSession, ids: List[int]) -> List[QuestionSchema]:
        return await self.delete_bulk(session, ids=ids)


crud_question = CRUDQuestion(Question)
