from fastapi import Request, Response, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_user
from app.models import User
from app.core import get_settings
from app.schemas import UserCreateSchema, UserLoginSchema
from app.utils import hash_password, create_access_token, send_refresh_token, verify_password, decode_token, \
    clear_refresh_token

settings = get_settings()


class AuthService:
    @staticmethod
    async def register(schema: UserCreateSchema, response: Response, session: AsyncSession):
        # check email
        user = await crud_user.find_one_by_email(email=schema.email, session=session)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail={"email": "Email đã tồn tại!"})

        # insert to table
        schema.password = hash_password(schema.password)
        created_user = await crud_user.create_one(schema=schema, session=session)

        # generate token
        access_token = create_access_token(user=created_user)

        # send refresh token
        send_refresh_token(response=response, user=created_user)
        return {"user": created_user.to_dict(un_selects=["password"]), "access_token": access_token}

    @staticmethod
    async def login(schema: UserLoginSchema, response: Response, session: AsyncSession):
        # check user
        user = await crud_user.find_one_by_email(email=schema.email, session=session)

        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Tên người dùng hoặc mật khẩu không chính xác!")

        if not verify_password(schema.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Tên người dùng hoặc mật khẩu không chính xác!")

        # generate token
        access_token = create_access_token(user=user)

        # send refresh token
        send_refresh_token(response=response, user=user)

        return {"user": user.to_dict(un_selects=["password"]), "access_token": access_token}

    @staticmethod
    async def refresh_token(request: Request, response: Response, session: AsyncSession):
        token = request.cookies.get(settings.REFRESH_TOKEN_COOKIE_NAME)
        if not token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token không hợp lệ!")

        try:
            user_decode = decode_token(token=token)
            user = await crud_user.find_one_by_id(id=int(user_decode['user_id']), session=session)
            if not user or user.token_version != user_decode['token_version']:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token không hợp lệ!")

            access_token = create_access_token(user=user)

            # send refresh token
            send_refresh_token(response=response, user=user)
            return {"access_token": access_token}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token không hợp lệ!")

    @staticmethod
    async def logout(response: Response, user_decode: dict, session: AsyncSession):
        # check username
        user = await crud_user.find_one_by_id(id=user_decode.get('user_id'), session=session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Người dùng không tồn tại!")

        await crud_user.update_token_version(id=user.id, token_version=user.token_version + 1, session=session)
        clear_refresh_token(response=response)
