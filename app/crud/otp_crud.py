from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import OTP
from app.schemas import OTPSchema, OTPCreateSchema, \
    OTPUpdateSchema


class CRUDOTP(CRUDBase[OTPSchema, OTPCreateSchema, OTPUpdateSchema]):
    async def create_one(self, otp_data: OTPCreateSchema, session: AsyncSession):
        return await self.create(session, obj_in=otp_data)

    async def update_one(
        self, id: int, otp_data: OTPUpdateSchema, session: AsyncSession
    ) -> Optional[OTP]:
        otp = await self.get(session, id=id)

        if otp:
            await self.update(session, obj_in=otp_data, db_obj=otp)

        return otp


crud_otp = CRUDOTP(OTP)
