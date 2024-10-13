from pydantic import BaseModel, HttpUrl
from uuid import UUID
from typing import List, Optional

class MediaBase(BaseModel):
    url: HttpUrl 
    type: str     # MIME-type (image/jpeg, video/mp4)
    size: int     # in bytes 

class MediaCreate(MediaBase):
    pass

class MediaUpdate(BaseModel):
    url: Optional[HttpUrl]
    type: Optional[str]
    size: Optional[int]

class MediaResponse(MediaBase):
    id: UUID

class DeleteResponse(BaseModel):
    message: str

class PaginatedMediaList(BaseModel):
    total: int
    page: int
    size: int
    media: List[MediaResponse]
