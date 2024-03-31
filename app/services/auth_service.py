from fastapi import Request, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.crud import crud_user
from app.enums import EmailEnum
from app.schemas import UserCreateSchema, UserLoginSchema
from app.utils import hash_password, create_access_token, send_refresh_token, verify_password, decode_token, \
    clear_refresh_token, send_email
from app.utils.jwt_util import create_email_token

settings = get_settings()


class AuthService:
    @staticmethod
    async def register(request: Request, user_data: UserCreateSchema, response: Response, session: AsyncSession):
        # check email
        user = await crud_user.find_one_by_email(email=user_data.email, session=session)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail={"email": "Email đã tồn tại!"})

        # insert to table
        user_data.password = hash_password(user_data.password)
        created_user = await crud_user.create_one(user_data=user_data, session=session)

        # generate token
        access_token = create_access_token(user=created_user)

        # send refresh token
        send_refresh_token(response=response, user=created_user)

        # send mail
        email_token = create_email_token(user=created_user)
        url = settings.CLIENT_URL + "/xac-minh-email/" + email_token

        await send_email(email_type=EmailEnum.VERIFY, emails=[created_user.email],
                         data={"request": request, "verify_link": url, "fullname": created_user.fullname})
        return {"user": created_user.dict(un_selects=["password"]), "access_token": access_token}

    @staticmethod
    async def login(user_data: UserLoginSchema, response: Response, session: AsyncSession):
        # check user
        user = await crud_user.find_one_by_email(email=user_data.email, session=session)

        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={"email": "Email hoặc mật khẩu không chính xác!",
                                        "password": "Email hoặc mật khẩu không chính xác!"})

        if not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail={"email": "Email hoặc mật khẩu không chính xác!",
                                                                 "password": "Email hoặc mật khẩu không chính xác!"})

        # generate token
        access_token = create_access_token(user=user)

        # send refresh token
        send_refresh_token(response=response, user=user)

        return {"user": user.dict(un_selects=["password"]), "access_token": access_token}

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
    async def logout(response: Response, id: int, session: AsyncSession):
        # check username
        user = await crud_user.find_one_by_id(id=id, session=session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Người dùng không tồn tại!")

        await crud_user.update_token_version(id=user.id, token_version=user.token_version + 1, session=session)
        clear_refresh_token(response=response)
