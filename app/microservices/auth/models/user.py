import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Enum, String
from app.microservices.auth.core.roles import DEFAULT_ROLE, Role
from app.microservices.auth.utils.db import AuthBase

class User(AuthBase):
    __tablename__ = "users"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=DEFAULT_ROLE)
    