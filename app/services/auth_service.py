from datetime import datetime, timedelta

from fastapi import Request, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.crud import crud_user, crud_otp
from app.enums import EmailEnum
from app.schemas import UserCreateSchema, UserLoginSchema, UserForgotPasswordSchema, UserOTPPasswordSchema, \
    OTPCreateSchema, OTPUpdateSchema
from app.utils import hash_password, create_access_token, send_refresh_token, verify_password, decode_token, \
    clear_refresh_token, send_email, verify_otp, generate_otp
from app.utils.jwt_util import create_email_token

settings = get_settings()


class AuthService:
    @staticmethod
    async def register(request: Request, user_data: UserCreateSchema, response: Response, session: AsyncSession):
        # check email
        user = await crud_user.find_one_by_email(email=user_data.email, session=session)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email đã tồn tại!")

        # insert to table
        user_data.password = hash_password(user_data.password)
        created_user = await crud_user.create_one(user_data=user_data, session=session)

        # send mail
        email_token = create_email_token(user=created_user)
        url = settings.CLIENT_URL + "/xac-minh-email?token=" + email_token

        await send_email(email_type=EmailEnum.VERIFY, emails=[created_user.email],
                         data={"request": request, "verify_link": url, "fullname": created_user.fullname})

        # generate token
        access_token = create_access_token(user=created_user)

        # send refresh token
        send_refresh_token(response=response, user=created_user)

        return {"user": created_user.dict(), "access_token": access_token}

    @staticmethod
    async def verify_email(token: str, response: Response, session: AsyncSession):
        user_decode = decode_token(token=token)
        if not user_decode:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ!")

        user = await crud_user.find_one_by_id(id=user_decode.get("user_id"), session=session)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ!")

        if user.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài khoản đã xác minh email!")

        updated_user = await crud_user.verify_email(id=user.id, session=session)

        # generate token
        access_token = create_access_token(user=updated_user)

        # send refresh token
        send_refresh_token(response=response, user=updated_user)

        return {"user": updated_user.dict(), "access_token": access_token}

    @staticmethod
    async def resend_email(user_id: int, request: Request, session: AsyncSession):
        user = await crud_user.find_one_by_id(id=user_id, session=session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản!")

        if user.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài khoản đã xác minh email!")

        # send mail
        email_token = create_email_token(user=user)
        url = settings.CLIENT_URL + "/xac-minh-email?token=" + email_token

        await send_email(email_type=EmailEnum.VERIFY, emails=[user.email],
                         data={"request": request, "verify_link": url, "fullname": user.fullname})

    @staticmethod
    async def refresh_otp(email: str, request: Request, session: AsyncSession):
        user = await crud_user.find_one_by_email(email=email, session=session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản!")

        if not user.otp:
            otp_code = generate_otp(settings.OTP_LIMITED)
            otp_data = OTPCreateSchema(code=otp_code, limited=settings.OTP_LIMITED, user_id=user.id)
            await crud_otp.create_one(otp_data=otp_data, session=session)
        else:
            # check otp
            current_date = datetime.now()
            # blocked otp
            if current_date - user.otp.modified_at <= timedelta(minutes=settings.OTP_EXPIRE_MINUTES):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Vui lòng thử lại sau {settings.OTP_EXPIRE_MINUTES - int((current_date - user.otp.modified_at).total_seconds() / 60)} phút!")

            # limited otp
            if current_date - user.otp.modified_at <= timedelta(days=1) and user.otp.limited == 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Bạn đã hết lượt trong ngày hôm nay, vui lòng thử lại vào ngày mai!")
            if current_date - user.otp.modified_at > timedelta(days=1):
                user.otp.limited = settings.OTP_LIMITED

            # generate otp
            user.otp.limited -= 1
            otp_code = generate_otp(user.otp.limited)
            otp_data = OTPUpdateSchema(code=otp_code, limited=user.otp.limited)
            await crud_otp.update_one(id=user.otp.id, otp_data=otp_data, session=session)

        # send otp
        await send_email(email_type=EmailEnum.RESET_PASSWORD, emails=[user.email],
                         data={"request": request, "otp_code": otp_code, "otp_expire": settings.OTP_EXPIRE_MINUTES,
                               "fullname": user.fullname})

    @staticmethod
    async def forgot_password(user_data: UserForgotPasswordSchema, response: Response, session: AsyncSession):
        user = await crud_user.find_one_by_email(email=user_data.email, session=session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản!")
        if user.otp.code != user_data.otp:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP không hợp lệ!")
        user.password = hash_password(password=user_data.new_password)

        # generate token
        access_token = create_access_token(user=user)

        # send refresh token
        send_refresh_token(response=response, user=user)

        return {"user": user.dict(), "access_token": access_token}

    @staticmethod
    async def send_otp_password(email: str, request: Request, session: AsyncSession):
        user = await crud_user.find_one_by_email(email=email, session=session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản!")

        if not user.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email chưa được xác minh!")

        await AuthService.refresh_otp(email=email, request=request, session=session)

    @staticmethod
    async def verify_otp_password(user_data: UserOTPPasswordSchema, session: AsyncSession):
        user = await crud_user.find_one_by_email(email=user_data.email, session=session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản!")

        # check otp
        current_date = datetime.now()
        if current_date - user.otp.modified_at > timedelta(minutes=settings.OTP_EXPIRE_MINUTES):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP đã hết hạn!")

        # verify email
        verify_success = verify_otp(user_data.otp, user.otp.limited)
        if not verify_success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP không hợp lệ hoặc đã sử dụng!")

    @staticmethod
    async def login(user_data: UserLoginSchema, response: Response, session: AsyncSession):
        # check user
        user = await crud_user.find_one_by_email(email=user_data.email, session=session)

        if not user or not verify_password(user_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email hoặc mật khẩu không chính xác!")

        # generate token
        access_token = create_access_token(user=user)

        # send refresh token
        send_refresh_token(response=response, user=user)

        return {"user": user.dict(), "access_token": access_token}

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
