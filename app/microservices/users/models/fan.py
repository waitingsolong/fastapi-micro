import uuid
from sqlalchemy import Column, ForeignKey, Table, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.microservices.users.utils.db import UsersBase

fan_favourite_players_association = Table(
    "fan_favourite_players",
    UsersBase.metadata,
    Column("fan_id", UUID(), ForeignKey("fans.id")),
    Column("player_id", UUID(), ForeignKey("players.id")),
)

fan_favourite_matches_association = Table(
    "fan_favourite_matches",
    UsersBase.metadata,
    Column("fan_id", UUID(), primary_key=True),  # Удален ForeignKey
    Column("match_id", UUID(), primary_key=True),  # Удален ForeignKey
)

fan_favourite_teams_association = Table(
    "fan_favourite_teams",
    UsersBase.metadata,
    Column("fan_id", UUID(), primary_key=True),  # Удален ForeignKey
    Column("team_id", UUID(), primary_key=True),  # Удален ForeignKey
)

fan_media_association = Table(
    "fan_media",
    UsersBase.metadata,
    Column("fan_id", UUID(), primary_key=True),  # Удален ForeignKey
    Column("media_id", UUID(), primary_key=True),  # Удален ForeignKey
)

class Fan(UsersBase):
    __tablename__ = "fans"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    avatar_url = Column(UUID(), nullable=True)
    
    favourite_players = relationship(
        "Player",
        secondary=fan_favourite_players_association,
        back_populates="fans",
    )
    
    def add_favourite_player(self, player_id: UUID) -> bool:
        if len(self.favourite_players) < 3:
            self.favourite_players.append(player_id)
            return True
        return False

    def add_favourite_match(self, match_id: UUID) -> bool:
        if len(self.favourite_matches) < 3:
            self.favourite_matches.append(match_id)
            return True
        return False

    def add_favourite_team(self, team_id: UUID) -> bool:
        if len(self.favourite_teams) < 3:
            self.favourite_teams.append(team_id)
            return True
        return False
