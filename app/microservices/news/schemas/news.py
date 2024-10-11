from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from enum import Enum
from uuid import UUID

class NewsCategory(str, Enum):
    articles = "articles"
    player_interviews = "player_interviews"
    transfer_announcements = "transfer_announcements"
    press_releases = "press_releases"

class CreateNewsSchema(BaseModel):
    title: str
    content: str
    category: NewsCategory
    author: Optional[str]
    media: Optional[List[HttpUrl]] = []
    tags: List[str] = []  

class UpdateNewsSchema(BaseModel):
    title: Optional[str]
    content: Optional[str]
    category: Optional[NewsCategory]
    media: Optional[List[HttpUrl]] = []
    tags: Optional[List[str]] = []
