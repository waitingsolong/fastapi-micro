from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from app.utils.models import Reaction

class EntityType(str, Enum):
    news = "news"
    post = "post"
    match = "match"
    
class CreateCommentRequest(BaseModel):
    content: str
    author: str
    entity_id: UUID
    entity_type: EntityType  

class CreateCommentResponse(BaseModel):
    comment_id: UUID
    content: str
    author: str
    created_at: datetime
    entity_id: UUID
    entity_type: EntityType

class CommentResponse(BaseModel):
    comment_id: UUID
    content: str
    author: str
    created_at: datetime
    updated_at: Optional[datetime]
    updated: bool
    reactions: Optional[List[Reaction]]
    replies: Optional[List[UUID]] 
    entity_id: UUID
    entity_type: EntityType

class UpdateCommentRequest(BaseModel):
    content: Optional[str] = None
    updated: bool = True

class UpdateCommentResponse(BaseModel):
    comment_id: UUID
    content: str
    updated_at: datetime
    updated: bool

class DeleteCommentResponse(BaseModel):
    message: str

class AddReactionRequest(BaseModel):
    emoji: str

class AddReactionResponse(BaseModel):
    message: str
    reaction: Reaction
    
class GetRepliesResponse(BaseModel):
    replies: List[CommentResponse]
    total: int
