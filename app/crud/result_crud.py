from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Result
from app.schemas import ResultSchema, ResultCreateSchema, \
    ResultUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Result
from app.schemas import ResultSchema, ResultCreateSchema, \
    ResultUpdateSchema


class CRUDResult(CRUDBase[ResultSchema, ResultCreateSchema, ResultUpdateSchema]):
    async def create_one(self, result_data: ResultCreateSchema, session: AsyncSession):
        return await self.create(session, obj_in=result_data)


crud_result = CRUDResult(Result)
