import yadisk
from uuid import uuid4
from fastapi import UploadFile
from app.microservices.media.core.config import settings
import os

y = yadisk.YaDisk(token=settings.YANDEX_DISK_API_KEY)

MEDIA_TMP_FOLDER = os.path.join(settings.ROOT_DIR, "data/media/tmp/")

os.makedirs(MEDIA_TMP_FOLDER, exist_ok=True)

async def save_media_file(file: UploadFile) -> str:
    unique_filename = f"{uuid4()}_{file.filename}"
    temp_path = os.path.join(MEDIA_TMP_FOLDER, unique_filename)

    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)

    remote_path = f"disk:/media/{unique_filename}"

    with open(temp_path, "rb") as f:
        y.upload(f, remote_path)

    os.remove(temp_path)

    file_url = y.get_download_link(remote_path)
    
    return file_url

def delete_media_file(file_url: str):
    try:
        remote_path = file_url.replace("https://", "").split("/", 1)[1]
        y.remove(f"disk:/{remote_path}")
    except yadisk.exceptions.PathNotFoundError:
        raise Exception("File not found on Yandex Disk")
    except Exception as e:
        raise Exception(f"Failed to delete file from Yandex Disk: {str(e)}")
