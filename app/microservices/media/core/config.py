import logging
from pathlib import Path
from typing import Optional
from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_DB: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[SecretStr] = None
    POSTGRES_URI: Optional[str] = "postgresql+asyncpg://postgres:@db/media"
    
    # defaulted 
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent.parent
    print(f"ROOT_DIR: {ROOT_DIR}")
    
    class Config:
        env_file = Path(__file__).resolve().parent.parent / '.env'

def init_settings():
    settings = Settings()
    if settings.POSTGRES_URI is None and all(
        [settings.POSTGRES_USER, settings.POSTGRES_PASSWORD, settings.POSTGRES_HOST, settings.POSTGRES_DB]
    ):
        settings.POSTGRES_URI = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD.get_secret_value()}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}"
    elif not settings.POSTGRES_URI:
        logging.error("Media DB is not initialized. Please provide POSTGRES_URI in .env file")
    return settings

settings = init_settings()
