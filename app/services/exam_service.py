from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.crud import crud_exam
from app.utils import to_list_dict

settings = get_settings()


class ExamService:
    @staticmethod
    async def get_list_by_user_id(user_id: int, session: AsyncSession):
        tests = await crud_exam.find_list_by_user_id(user_id=user_id, session=session)
        return {"exams": to_list_dict(objects=tests)}
