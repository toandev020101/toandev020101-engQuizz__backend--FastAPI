from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.crud import crud_question, crud_answer
from app.schemas import QuestionCreateSchema, QuestionUpdateSchema
from app.utils import to_list_dict

settings = get_settings()


class QuestionService:
    @staticmethod
    async def count_all(session: AsyncSession):
        count = await crud_question.count_all(session=session)
        return {"count": count}

    @staticmethod
    async def get_all(session: AsyncSession):
        questions = await crud_question.find_all(session=session)
        return {"questions": to_list_dict(objects=questions, )}

    @staticmethod
    async def get_pagination(_limit: int, _page: int, search_term: str, level: str,
                             session: AsyncSession):
        questions = await crud_question.find_pagination(_limit=_limit, _page=_page, search_term=search_term,
                                                        level=level, session=session)

        total = await crud_question.count_all(session=session)
        return {"questions": to_list_dict(objects=questions), "total": total}

    @staticmethod
    async def get_one_by_id(id: int, session: AsyncSession):
        question = await crud_question.find_one_by_id(id=id, session=session)

        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy câu hỏi!")

        return {"question": question.dict()}

    @staticmethod
    async def add_one(creator_id: int, question_data: QuestionCreateSchema, session: AsyncSession):
        question = await crud_question.find_one_by_content(content=question_data.content, session=session)

        if question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Nội dung đã tồn tại!")

        question_data_answers = question_data.answers
        del question_data.answers
        question_data.creator_id = creator_id
        created_question = await crud_question.create_one(question_data=question_data, session=session)
        await crud_answer.create_list(question_id=created_question.id, answers_data=question_data_answers,
                                      session=session)
        return {"question": created_question.dict()}

    @staticmethod
    async def add_list(creator_id: int, questions_data: List[QuestionCreateSchema], session: AsyncSession):
        for question_data in questions_data:
            question = await crud_question.find_one_by_content(content=question_data.content, session=session)

            if question:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Nội dung đã tồn tại!")

        created_questions = []
        for question_data in questions_data:
            question_data_answers = question_data.answers
            del question_data.answers
            question_data.creator_id = creator_id
            created_question = await crud_question.create_one(question_data=question_data, session=session)
            await crud_answer.create_list(question_id=created_question.id, answers_data=question_data_answers,
                                          session=session)
            created_questions.append(created_question)
        return {"questions": to_list_dict(objects=created_questions)}

    @staticmethod
    async def update_one(id: int, question_data: QuestionUpdateSchema, session: AsyncSession):
        question = await crud_question.find_one_by_id(id=id, session=session)

        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Không tìm thấy câu hỏi!")

        question_data_answers = question_data.answers
        del question_data.answers
        updated_question = await crud_question.update_one(id=id, question_data=question_data, session=session)

        await crud_answer.delete_list_by_question_id(question_id=updated_question.id, session=session)
        await crud_answer.create_list(question_id=updated_question.id, answers_data=question_data_answers,
                                      session=session)
        return {"question": updated_question.dict()}

    @staticmethod
    async def remove_one(id: int, session: AsyncSession):
        removed_question = await crud_question.delete_one(id=id, session=session)
        if not removed_question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy câu hỏi!")
        return removed_question.dict()

    @staticmethod
    async def remove_list(ids: List[int], session: AsyncSession):
        removed_questions = await crud_question.delete_list(ids=ids, session=session)
        if not removed_questions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy câu hỏi!")
        return to_list_dict(objects=removed_questions, )
