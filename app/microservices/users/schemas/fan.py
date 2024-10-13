from pydantic import BaseModel, UUID4, HttpUrl
from typing import List, Optional


class FanBase(BaseModel):
    avatar_url: Optional[HttpUrl] = None
    favourite_players: Optional[List[UUID4]] = None
    favourite_matches: Optional[List[UUID4]] = None
    favourite_teams: Optional[List[UUID4]] = None

    class Config:
        orm_mode = True


class FanCreate(FanBase):
    pass


class FanUpdate(FanBase):
    pass


class FanResponse(FanBase):
    id: UUID4


class FanListResponse(BaseModel):
    fans: List[FanResponse]
    total: int
