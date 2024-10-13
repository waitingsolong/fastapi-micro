from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.microservices.media.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.POSTGRES_URI 

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

MediaBase = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
        