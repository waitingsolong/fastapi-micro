import uuid
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.utils.models import Reaction

class Comment(BaseModel):
    content: str
    author: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    updated: bool = False
    reactions: Optional[List[Reaction]] = []
    replies: Optional[List[uuid.UUID]] = []
    entity_id: uuid.UUID
    entity_type: str  
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
        }
    