from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID
from datetime import datetime

from pymongo import ReturnDocument
from app.microservices.comments.schemas.comments import (
    CreateCommentRequest, CreateCommentResponse, 
    CommentResponse, UpdateCommentRequest, UpdateCommentResponse, 
    AddReactionRequest, AddReactionResponse, EntityType, GetRepliesResponse
)
from uuid import uuid4

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

async def get_mongo_client():
    from app.utils.mongo import get_collection
    return await get_collection("comments")

@router.post("/", response_model=CreateCommentResponse)
async def create_comment(comment: CreateCommentRequest):
    db = await get_mongo_client()
    
    new_comment = comment.model_dump()
    new_comment["_id"] = uuid4()  # Changed to use ObjectId
    new_comment["created_at"] = datetime.utcnow()
    new_comment["reactions"] = []
    new_comment["replies"] = []
    
    await db["comments"].insert_one(new_comment)
    
    return CreateCommentResponse(
        comment_id=new_comment["_id"],  # Changed to use ObjectId
        content=new_comment["content"],
        author=new_comment["author"],
        created_at=new_comment["created_at"],
        entity_id=new_comment["entity_id"],
        entity_type=new_comment["entity_type"]
    )

@router.get("/{entity_id}", response_model=List[CommentResponse])
async def get_comments(entity_id: UUID, entity_type: EntityType):
    db = await get_mongo_client()
    comments = await db["comments"].find({"entity_id": entity_id, "entity_type": entity_type}).to_list(length=100)
    if not comments:
        raise HTTPException(status_code=404, detail="Комментарии не найдены")
    return comments

@router.patch("/{comment_id}", response_model=UpdateCommentResponse)
async def update_comment(comment_id: UUID, comment: UpdateCommentRequest):
    db = await get_mongo_client()
    
    # Update comment and set updated_at
    update_data = comment.model_dump(exclude_unset=True)
    if "content" in update_data:
        update_data["updated_at"] = datetime.utcnow()
    
    updated_comment = await db["comments"].find_one_and_update(
        {"_id": comment_id},  # Changed to use ObjectId
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )
    
    if updated_comment:
        return UpdateCommentResponse(
            comment_id=updated_comment["_id"],  # Changed to use ObjectId
            content=updated_comment["content"],
            updated_at=updated_comment["updated_at"],
            updated=updated_comment["updated"]
        )
    raise HTTPException(status_code=404, detail="Комментарий не найден")

@router.post("/{comment_id}/reaction", response_model=AddReactionResponse)
async def add_reaction(comment_id: UUID, reaction: AddReactionRequest):
    db = await get_mongo_client()
    
    # Find if the reaction already exists for the comment
    existing_comment = await db["comments"].find_one({"_id": comment_id, "reactions.emoji": reaction.emoji})  # Changed to use ObjectId
    
    if existing_comment:
        # Increment existing reaction count
        result = await db["comments"].update_one(
            {"_id": comment_id, "reactions.emoji": reaction.emoji},  # Changed to use ObjectId
            {"$inc": {"reactions.$.count": 1}}
        )
    else:
        # Add a new reaction
        result = await db["comments"].update_one(
            {"_id": comment_id},  # Changed to use ObjectId
            {"$push": {"reactions": {"emoji": reaction.emoji, "count": 1}}}
        )
    
    if result.modified_count == 1:
        return AddReactionResponse(message="Reaction added", reaction={"emoji": reaction.emoji, "count": 1})
    
    raise HTTPException(status_code=404, detail="Comment not found")

@router.get("/{comment_id}/replies", response_model=GetRepliesResponse)
async def get_replies(comment_id: UUID, skip: int = 0, limit: int = 10):
    db = await get_mongo_client()

    comment = await db["comments"].find_one({"_id": comment_id})  # Changed to use ObjectId
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")

    reply_ids = comment.get("replies", [])  # Changed to retrieve replies list
    replies = await db["comments"].find({"_id": {"$in": reply_ids}}).skip(skip).limit(limit).to_list(length=limit)
    
    return GetRepliesResponse(replies=replies)
