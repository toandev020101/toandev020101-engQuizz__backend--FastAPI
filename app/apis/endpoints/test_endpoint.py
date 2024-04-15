from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends import get_session, check_auth
from app.core import get_settings
from app.schemas import ResponseSchema, RemoveSchema, TestCreateSchema, TestUpdateSchema
from app.services import TestService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/test", tags=["Test"])


@router.get("", response_model=ResponseSchema)
async def get_test_pagination(_limit: int = 5, _page: int = 0, search_term: str = "", status_test: str = "all",
                              session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    data = await TestService.get_pagination(_limit=_limit, _page=_page, search_term=search_term,
                                            status_test=status_test,
                                            session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách đề thi thành công", data=data)


@router.get("/count-all", response_model=ResponseSchema)
async def count_test_all(session: AsyncSession = Depends(get_session),
                       user_decode=Depends(check_auth)):
    data = await TestService.count_all(session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy số lượng đề thi thành công", data=data)


@router.get("/{id}", response_model=ResponseSchema)
async def get_test_one_by_id(id: int, session: AsyncSession = Depends(get_session),
                             user_decode=Depends(check_auth)):
    data = await TestService.get_one_by_id(id=id, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy thông tin đề thi thành công", data=data)


@router.post("", response_model=ResponseSchema)
async def add_test_one(test_data: TestCreateSchema,
                       session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    await TestService.add_one(creator_id=user_decode.get("user_id"), test_data=test_data, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thêm đề thi thành công")


@router.put("/{id}", response_model=ResponseSchema)
async def update_test_one(id: int, test_data: TestUpdateSchema,
                          session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    await TestService.update_one(id=id, test_data=test_data, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Cập nhật đề thi thành công")


@router.delete("/{id}", response_model=ResponseSchema)
async def remove_test_one(id: int, session: AsyncSession = Depends(get_session), user_decode=Depends(check_auth)):
    data = await TestService.remove_one(id=id, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa đề thi thành công", data=data)


@router.delete("", response_model=ResponseSchema)
async def remove_test_list(remove_data: RemoveSchema, session: AsyncSession = Depends(get_session),
                           user_decode=Depends(check_auth)):
    data = await TestService.remove_list(ids=remove_data.ids, session=session)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa danh sách đề thi thành công", data=data)
