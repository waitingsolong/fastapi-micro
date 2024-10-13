from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List
from app.microservices.news.schemas.news import CreateNews, UpdateNews
from app.microservices.news.models.news import News
from app.microservices.comments.models.comments import Comment
from app.utils.models import Reaction
from pymongo import ReturnDocument
from uuid import uuid4

router = APIRouter(
    prefix="/news",
    tags=["news"]
)

async def get_mongo_client():
    from app.utils.mongo import get_collection
    return await get_collection("news")

@router.get("/{news_id}", response_model=News)
async def get_news(news_id: UUID):
    db = await get_mongo_client()

    news = await db["news"].find_one({"news_id": news_id})
    
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    comments = await db["comments"].find({"_id": {"$in": news["comments"]}}).to_list(length=100)

    news["comments"] = comments

    return news


@router.post("/", response_model=News)
async def create_news(news: CreateNews):
    db = await get_mongo_client()
    new_news = News(**news.model_dump())
    result = await db["news"].insert_one(new_news.model_dump())
    if result.acknowledged:
        return new_news
    raise HTTPException(status_code=400, detail="Ошибка создания новости")


@router.get("/", response_model=List[News])
async def list_news(limit: int = Query(50, ge=1), offset: int = 0):
    db = await get_mongo_client()
    news_list = await db["news"].find().skip(offset).limit(limit).to_list(limit)
    return news_list


@router.put("/{news_id}", response_model=News)
async def update_news(news_id: UUID, news: UpdateNews):
    db = await get_mongo_client()
    updated_news = await db["news"].find_one_and_update(
        {"news_id": news_id},
        {"$set": news.model_dump(exclude_unset=True)},
        return_document=ReturnDocument.AFTER
    )
    if updated_news:
        return updated_news
    raise HTTPException(status_code=404, detail="Новость не найдена")


@router.delete("/{news_id}/comments/{comment_id}")
async def delete_news_comment(news_id: UUID, comment_id: UUID):
    db = await get_mongo_client()

    result = await db["news"].update_one(
        {"news_id": news_id},
        {"$pull": {"comments": comment_id}}
    )

    if result.modified_count == 1:
        await db["comments"].delete_one({"_id": comment_id})
        return {"message": "Комментарий удалён"}
    
    raise HTTPException(status_code=404, detail="Комментарий не найден")


@router.post("/{news_id}/comment", response_model=Comment)
async def add_comment(news_id: UUID, comment: Comment):
    db = await get_mongo_client()

    comment_id = uuid4()
    await db["comments"].insert_one({"_id": comment_id, **comment.model_dump()})

    result = await db["news"].update_one(
        {"news_id": news_id},
        {"$push": {"comments": comment_id}} 
    )

    if result.modified_count == 1:
        return comment
    raise HTTPException(status_code=404, detail="Новость не найдена")


@router.post("/{news_id}/reaction")
async def add_reaction(news_id: UUID, reaction: Reaction):
    db = await get_mongo_client()
    
    existing_news = await db["news"].find_one({"news_id": news_id, "reactions.reaction": reaction.reaction})
    
    if existing_news:
        result = await db["news"].update_one(
            {"news_id": news_id, "reactions.reaction": reaction.reaction},
            {"$inc": {"reactions.$.count": 1}}
        )
    else:
         result = await db["news"].update_one(
            {"news_id": news_id},
            {"$push": {"reactions": {"reaction": reaction.reaction, "count": 1}}}
        )
    
    if result.modified_count == 1:
        return {"message": "Реакция добавлена"}
    
    raise HTTPException(status_code=404, detail="Новость не найдена")
