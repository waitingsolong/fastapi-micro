from fastapi import APIRouter, File, HTTPException, UploadFile
from uuid import UUID
from app.microservices.media.models.media import Media
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.microservices.media.schemas.media import MediaCreate, MediaUpdate, MediaResponse, DeleteResponse, PaginatedMediaList
from app.microservices.media.utils.db import get_db
from app.microservices.media.utils.storage.yandex_disk import delete_media_file
from app.microservices.media.utils.storage.file_storage import save_media_file as save_media_file_filestorage
from app.microservices.media.utils.storage.yandex_disk import save_media_file as save_media_file_yadisk
from app.microservices.media.core.config import settings

save_media_file = None 
if settings.YANDEX_DISK_API_KEY:
    save_media_file = save_media_file_yadisk
else:
    save_media_file = save_media_file_filestorage

router = APIRouter(
    prefix="/media",
    tags=["media"]
)

@router.post("/", response_model=MediaResponse)
def create_media(media: MediaCreate, db: Session = Depends(get_db)):
    db_media = Media(url=media.url, type=media.type, size=media.size)
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media

@router.put("/{media_id}", response_model=MediaResponse)
def update_media(media_id: UUID, media: MediaUpdate, db: Session = Depends(get_db)):
    db_media = db.query(Media).filter(Media.id == media_id).first()
    if not db_media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    for key, value in media.dict(exclude_unset=True).items():
        setattr(db_media, key, value)
    
    db.commit()
    db.refresh(db_media)
    return db_media

@router.get("/{media_id}", response_model=MediaResponse)
def get_media(media_id: UUID, db: Session = Depends(get_db)):
    db_media = db.query(Media).filter(Media.id == media_id).first()
    if not db_media:
        raise HTTPException(status_code=404, detail="Media not found")
    return db_media

@router.delete("/{media_id}", response_model=DeleteResponse)
def delete_media(media_id: UUID, db: Session = Depends(get_db)):
    db_media = db.query(Media).filter(Media.id == media_id).first()
    if not db_media:
        raise HTTPException(status_code=404, detail="Media not found")

    try:
        delete_media_file(db_media.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting media from Yandex Disk: {str(e)}")

    db.delete(db_media)
    db.commit()
    return DeleteResponse(message="Media deleted successfully")

@router.get("/", response_model=PaginatedMediaList)
def list_media(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    total = db.query(Media).count()
    media_items = db.query(Media).offset(skip).limit(limit).all()
    return PaginatedMediaList(total=total, page=skip // limit + 1, size=len(media_items), media=media_items)

@router.post("/upload/", response_model=MediaResponse)
async def upload_media(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_url = await save_media_file(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to Yandex Disk: {str(e)}")
    
    db_media = Media(url=file_url, type=file.content_type, size=file.spool_max_size)
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    
    return db_media
