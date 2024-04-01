import os
from datetime import datetime

import aiofiles
from fastapi import UploadFile

from app.core import get_settings

settings = get_settings()


async def save_file(file: UploadFile):
    file_ext = file.filename.split(".")[-1]
    filename = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.{file_ext}"
    save_dir = os.path.join(settings.UPLOAD_ROOT, datetime.now().strftime('%Y/%m'))
    os.makedirs(save_dir, exist_ok=True)
    os.chmod(save_dir, 0o777)
    save_path = os.path.join(save_dir, filename)
    async with aiofiles.open(save_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    return f"/uploads/{datetime.now().strftime('%Y/%m')}/{filename}"
