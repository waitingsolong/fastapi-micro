from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, HttpUrl

class MatchResponse(BaseModel):
    id: UUID

class GetMatchResponse(BaseModel):
    date: Optional[str]    
    location: Optional[str]
    name: str  
    team1Logo: HttpUrl
    team1Name: str
    team1Points: Optional[int]
    team2Logo: HttpUrl
    team2Name: str
    team2Points: Optional[int]

class CreateMatchRequest(BaseModel):
    date: Optional[str]     
    location: Optional[str] 
    name: Optional[str]  
    team1id: UUID
    team2id: UUID

class UpdateMatchRequest(BaseModel):
    team1Points: Optional[int] = None
    team2Points: Optional[int] = None

class MatchListResponse(BaseModel):
    matches: List[MatchResponse]  
    total: int