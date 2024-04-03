from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends import get_session, check_auth
from app.core import get_settings
from app.schemas import ResponseSchema, RemoveSchema, QuestionCreateSchema, QuestionUpdateSchema
from app.services import QuestionService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/question", tags=["Question"])


@router.get("", response_model=ResponseSchema)
async def get_question_pagination(_limit: int = 5, _page: int = 0, search_term: str = "", level: str = "all",
                                  session: AsyncSession = Depends(get_session)):
    data = await QuestionService.get_pagination(_limit=_limit, _page=_page, search_term=search_term, level=level,
                                                session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách câu hỏi thành công", data=data)


@router.get("/{id}", response_model=ResponseSchema)
async def get_question_one_by_id(id: int, session: AsyncSession = Depends(get_session)):
    data = await QuestionService.get_one_by_id(id=id, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy thông tin câu hỏi thành công", data=data)


@router.post("", response_model=ResponseSchema)
async def add_question_one(question_data: QuestionCreateSchema,
                           session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    await QuestionService.add_one(creator_id=user_decode.get("user_id"), question_data=question_data, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thêm câu hỏi thành công")


@router.post("/any", response_model=ResponseSchema)
async def add_question_list(questions_data: List[QuestionCreateSchema],
                            session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    await QuestionService.add_list(creator_id=user_decode.get("user_id"), questions_data=questions_data, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thêm danh sách câu hỏi thành công")


@router.put("/{id}", response_model=ResponseSchema)
async def update_question_one(id: int, question_data: QuestionUpdateSchema,
                              session: AsyncSession = Depends(get_session)):
    await QuestionService.update_one(id=id, question_data=question_data, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Cập nhật câu hỏi thành công")


@router.delete("/{id}", response_model=ResponseSchema)
async def remove_question_one(id: int, session: AsyncSession = Depends(get_session)):
    data = await QuestionService.remove_one(id=id, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa câu hỏi thành công", data=data)


@router.delete("", response_model=ResponseSchema)
async def remove_question_list(remove_data: RemoveSchema, session: AsyncSession = Depends(get_session)):
    data = await QuestionService.remove_list(ids=remove_data.ids, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa danh sách câu hỏi thành công", data=data)
