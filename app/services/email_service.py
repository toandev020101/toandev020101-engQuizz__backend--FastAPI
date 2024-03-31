from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_user
from app.utils import decode_token


class EmailService:
    @staticmethod
    async def verify(token: str, session: AsyncSession):
        user_decode = decode_token(token=token)
        if not user_decode:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ!")

        user = await crud_user.find_one_by_id(id=user_decode.get("user_id"), session=session)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ!")

        if user.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài khoản đã xác minh email!")

        updated_user = await crud_user.verify_email(id=user.id, session=session)
        return updated_user.dict(un_selects=["password"])
