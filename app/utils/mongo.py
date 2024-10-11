from motor.motor_asyncio import AsyncIOMotorClient
from app.microservices.news.core.config import settings

MONGO_URI = settings.MONGO_URI
client = AsyncIOMotorClient(MONGO_URI)
db = client[settings.MONGO_DB_NAME]

async def get_collection(collection_name: str):
    return db[collection_name]
