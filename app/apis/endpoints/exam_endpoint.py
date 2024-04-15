from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends import get_session, check_auth
from app.core import get_settings
from app.schemas import ResponseSchema, RemoveSchema
from app.services import ExamService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/exam", tags=["Exam"])


@router.get("/all", response_model=ResponseSchema)
async def get_exam_all(session: AsyncSession = Depends(get_session),
                       user_decode=Depends(check_auth)):
    data = await ExamService.get_all(session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy tất cả bài thi thành công", data=data)


@router.get("/count-all", response_model=ResponseSchema)
async def count_exam_all(session: AsyncSession = Depends(get_session),
                         user_decode=Depends(check_auth)):
    data = await ExamService.count_all(session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy số lượng bài thi thành công", data=data)


@router.get("/submit", response_model=ResponseSchema)
async def get_exam_list_submit_by_user_id(session: AsyncSession = Depends(get_session),
                                          user_decode=Depends(check_auth)):
    data = await ExamService.get_list_submit_by_user_id(user_id=user_decode.get("user_id"), session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách bài thi thành công", data=data)


@router.get("/pagination", response_model=ResponseSchema)
async def get_exam_pagination(_limit: int = 5, _page: int = 0, search_term: str = "", score: str = "all",
                              correct_quantity: str = "all", session: AsyncSession = Depends(get_session),
                              user_decode=Depends(check_auth)):
    data = await ExamService.get_pagination(_limit=_limit, _page=_page, search_term=search_term, score=score,
                                            correct_quantity=correct_quantity, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách bài thi thành công", data=data)


@router.get("", response_model=ResponseSchema)
async def get_exam_list_by_user_id(session: AsyncSession = Depends(get_session),
                                   user_decode=Depends(check_auth)):
    data = await ExamService.get_list_by_user_id(user_id=user_decode.get("user_id"), session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách bài thi thành công", data=data)


@router.get("/{id}", response_model=ResponseSchema)
async def get_exam_one_by_id(id: int, session: AsyncSession = Depends(get_session),
                             user_decode=Depends(check_auth)):
    data = await ExamService.get_one_by_id(id=id, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy bài thi thành công", data=data)


@router.delete("/{id}", response_model=ResponseSchema)
async def remove_exam_one(id: int, session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    data = await ExamService.remove_one(id=id, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa bài thi thành công", data=data)


@router.delete("", response_model=ResponseSchema)
async def remove_exam_list(remove_data: RemoveSchema, session: AsyncSession = Depends(get_session),
                           user_decode=Depends(check_auth)):
    data = await ExamService.remove_list(ids=remove_data.ids, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa danh sách bài thi thành công", data=data)
