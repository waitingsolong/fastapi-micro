import aiofiles
import os
from fastapi import HTTPException, UploadFile
from app.microservices.media.core.config import settings 

MEDIA_FOLDER = os.path.join(settings.ROOT_DIR, "data/media/")

if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER)
    
    os.makedirs(MEDIA_FOLDER, exist_ok=True)

async def save_media_file(file: UploadFile) -> str:
    file_path = os.path.join(MEDIA_FOLDER, file.filename)

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(1024): 
                await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving media file: {str(e)}")

    return file_path
