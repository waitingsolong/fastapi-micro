from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from app.microservices.matches.utils.db import MatchBase

match_team_association = Table(
    'match_team',
    MatchBase.metadata,
    Column('match_id', UUID(), primary_key=True),
    Column('team_id', UUID(), nullable=False),
    Column('team_points', Integer, nullable=True, default=0)
)

match_players_association = Table(
    'match_players',
    MatchBase.metadata,
    Column('match_id', UUID(), primary_key=True),
    Column('player_id', UUID(), primary_key=True)
)

class Match(MatchBase):
    __tablename__ = 'matches'
    
    id = Column(UUID(), primary_key=True, default=uuid4, index=True, unique=True)
    name = Column(String, nullable=True)  
    date = Column(DateTime, nullable=True)  
    location = Column(String, nullable=True)

    @property
    def is_upcoming(self):
        return self.date > datetime.now() if self.date else False 
