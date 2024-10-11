import logging
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str = "comments"

    @property
    def MONGO_URI(self) -> str:
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB_NAME}"

    class Config:
        env_file = Path(__file__).resolve().parent.parent / '.env'

def init_settings():
    settings = Settings()
    return settings

settings = init_settings()
