from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.services import AuthService, EmailService
from app.apis.depends import check_auth, get_session
from app.schemas import ResponseSchema, UserCreateSchema, UserLoginSchema

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/auth", tags=["Authentication"])


@router.post("/register", response_model=ResponseSchema)
async def register(request: Request, user_data: UserCreateSchema, response: Response,
                   session: AsyncSession = Depends(get_session)):
    data = await AuthService.register(request=request, user_data=user_data, response=response, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Đăng ký thành công", data=data)


@router.get("/verify-email/{token}", response_model=ResponseSchema)
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
    data = await EmailService.verify(token=token, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xác minh email thành công", data=data)


@router.post("/login", response_model=ResponseSchema)
async def login(user_data: UserLoginSchema, response: Response, session: AsyncSession = Depends(get_session)):
    data = await AuthService.login(user_data=user_data, response=response, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK,
                          detail="Đăng nhập thành công",
                          data=data
                          )


@router.get("/refresh-token", response_model=ResponseSchema)
async def refresh_token(request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    data = await AuthService.refresh_token(request=request, response=response, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK,
                          detail="Refresh token thành công",
                          data=data
                          )


@router.get("/logout", response_model=ResponseSchema)
async def logout(response: Response, user_decode=Depends(check_auth), session: AsyncSession = Depends(get_session)):
    await AuthService.logout(response=response, id=user_decode.get("user_id"), session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Đăng xuất thành công")
