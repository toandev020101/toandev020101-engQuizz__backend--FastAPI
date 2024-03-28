from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.services import AuthService
from app.apis.depends import check_auth, get_session
from app.schemas import ResponseSchema, UserCreateSchema, UserLoginSchema

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/auth", tags=["Authentication"])


@router.post("/register", response_model=ResponseSchema)
async def register(request_body: UserCreateSchema, response: Response, session: AsyncSession = Depends(get_session)):
    data = await AuthService.register(schema=request_body, response=response, session=session)
    return ResponseSchema(code=status.HTTP_200_OK, message="Đăng ký thành công", data=data)


@router.post("/login", response_model=ResponseSchema)
async def login(request_body: UserLoginSchema, response: Response, session: AsyncSession = Depends(get_session)):
    data = await AuthService.login(schema=request_body, response=response, session=session)
    return ResponseSchema(code=status.HTTP_200_OK,
                          message="Đăng nhập thành công",
                          data=data
                          )


@router.get("/refresh-token", response_model=ResponseSchema)
async def refresh_token(request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    data = await AuthService.refresh_token(request=request, response=response, session=session)
    return ResponseSchema(code=status.HTTP_200_OK,
                          message="Lấy refresh token thành công",
                          data=data
                          )


@router.get("/logout", response_model=ResponseSchema)
async def logout(response: Response, user_decode=Depends(check_auth), session: AsyncSession = Depends(get_session)):
    await AuthService.logout(response=response, user_decode=user_decode, session=session)
    return ResponseSchema(code=status.HTTP_200_OK, message="Đăng xuất thành công")
