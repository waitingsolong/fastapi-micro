from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.microservices.media.utils.db import MediaBase

class Media(MediaBase):
    __tablename__ = "media"

    id = Column(UUID(), primary_key=True, default=uuid4)
    url = Column(String, nullable=False)
    type = Column(String, nullable=False)  # MIME-type
    size = Column(Integer, nullable=False)  # in bytes
