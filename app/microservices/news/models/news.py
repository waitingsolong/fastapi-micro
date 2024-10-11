import uuid
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.utils.models import Reaction

class News(BaseModel):
    news_id: UUID = Field(default_factory=UUID)
    title: str
    content: str
    category: str
    published_at: datetime = Field(default_factory=datetime.utcnow)
    author: Optional[str]
    media: Optional[List[HttpUrl]] = []
    reactions: Optional[List[Reaction]] = []
    comments: Optional[List[UUID]] = []
    tags: List[str] = []
