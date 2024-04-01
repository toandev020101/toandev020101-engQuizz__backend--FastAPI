from fastapi import APIRouter, status, UploadFile, File

from app.core import get_settings
from app.schemas import ResponseSchema
from app.utils import save_file

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/upload", tags=["Upload"])


@router.post("", response_model=ResponseSchema)
async def upload_file(file: UploadFile = File(...)):
    save_path = await save_file(file)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Tải tệp lên thành công", data={"path": save_path})
