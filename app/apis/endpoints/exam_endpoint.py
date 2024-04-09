from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends import get_session, check_auth
from app.core import get_settings
from app.schemas import ResponseSchema
from app.services import ExamService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/exam", tags=["Exam"])


@router.get("/", response_model=ResponseSchema)
async def get_exam_list_by_user_id(session: AsyncSession = Depends(get_session),
                                   user_decode=Depends(check_auth)):
    data = await ExamService.get_list_by_user_id(user_id=user_decode.get("user_id"), session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách bài thi thành công", data=data)
