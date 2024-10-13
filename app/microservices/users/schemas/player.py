from datetime import datetime
from pydantic import BaseModel, Field, field_validator, validator
from typing import Optional, List
from uuid import UUID
from app.microservices.users.models.player import PlayerPosition

class PlayerBase(BaseModel):
    full_name: Optional[str] = None
    weight: Optional[float] = Field(None, gt=0, description="Вес игрока в кг")
    height: Optional[float] = Field(None, gt=0, description="Рост игрока в см")
    date_of_birth: Optional[str] = None
    biography: Optional[str] = None
    goals: Optional[int] = Field(0, ge=0, description="Количество голов")
    matches_played: Optional[int] = Field(0, ge=0, description="Количество сыгранных матчей")
    number_in_club: Optional[int] = Field(None, ge=0, description="Игровой номер в клубе")
    role: Optional[PlayerPosition] = None

    class Config:
        orm_mode = True

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class Player(PlayerBase):
    id: UUID
    age: Optional[int] = None

    @field_validator('age', mode='before')
    def calculate_age(cls, value, values):
        date_of_birth = values.get('date_of_birth')
        if date_of_birth:
            return (datetime.now() - date_of_birth).days // 365
        return None

    class Config:
        orm_mode = True

class PlayerList(BaseModel):
    players: List[Player]
    total: int
    page: int
    size: int

    class Config:
        orm_mode = True

class PlayerDelete(BaseModel):
    id: UUID

    class Config:
        orm_mode = True
