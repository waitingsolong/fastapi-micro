from sqlalchemy import Column, String, Integer
from app.microservices.auth.core.db import Base
from app.microservices.auth.core.roles import Role

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default=Role.DEFAULT) 
    