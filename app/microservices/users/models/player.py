from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Integer, Float, Enum, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.microservices.users.utils.db import UsersBase
from sqlalchemy.orm import relationship


class PlayerPosition(str, PyEnum):
    forward = "Нападающий"
    defender = "Защитник"
    midfielder = "Полузащитник"
    goalkeeper = "Вратарь"
    retired = "Ушли"
    coach = "Тренер"

player_matches_association = Table(
    "player_matches",
    UsersBase.metadata,
    Column("player_id", UUID(), primary_key=True),  
    Column("match_id", UUID(), primary_key=True),   
)

# Ассоциация между игроками и командами
player_teams_association = Table(
    "player_teams",
    UsersBase.metadata,
    Column("player_id", UUID(), primary_key=True), 
    Column("team_id", UUID(), primary_key=True),   
)

class Player(UsersBase):
    __tablename__ = "players"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    weight = Column(Float, nullable=True)  
    height = Column(Float, nullable=True)  
    date_of_birth = Column(DateTime, nullable=False)
    biography = Column(String, nullable=True)  
    goals = Column(Integer, default=0, nullable=True)
    matches_played = Column(Integer, default=0, nullable=True)
    number_in_club = Column(Integer, nullable=True)  
    role = Column(Enum(PlayerPosition), nullable=False)
    
    teams = relationship(
        "Team",
        secondary=player_teams_association,
        back_populates="players",
        viewonly=True 
    )
    
    matches = relationship(
        "Match",
        secondary=player_matches_association,
        back_populates="players",
        viewonly=True  
    )
    