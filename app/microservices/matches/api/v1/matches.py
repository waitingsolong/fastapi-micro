from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID, uuid4
from sqlalchemy import extract, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.microservices.matches.models.matches import Match
from app.microservices.matches.schemas.matches import (
    MatchResponse,
    CreateMatchRequest,
    MatchListResponse,
    UpdateMatchRequest
)
from app.microservices.matches.schemas.matches import GetMatchResponse
from app.microservices.matches.utils.db import get_db

router = APIRouter(
    prefix="/matches",
    tags=["matches"]
)

@router.post("/", response_model=MatchResponse)
async def create_match(
    match_request: CreateMatchRequest, 
    db: AsyncSession = Depends(get_db)
):
    pass 

    match = Match(
        id=uuid4(),
        team1id=match_request.team1id,
        team2id=match_request.team2id,
        team1Points=match_request.team1Points,
        team2Points=match_request.team2Points,
        date=match_request.date,        
        location=match_request.location,
    )
    db.add(match)
    await db.commit()
    await db.refresh(match)
    return MatchResponse(id=match.id)

@router.get("/", response_model=MatchListResponse)
async def list_matches(
    skip: int = 0, 
    limit: int = 10, 
    db: AsyncSession = Depends(get_db)
):
    pass 
    result = await db.execute(
        select(Match).offset(skip).limit(limit)
    )
    matches = result.scalars().all()

    total = await db.scalar(select(func.count(Match.id))) 
    return MatchListResponse(matches=[MatchResponse(id=match.id) for match in matches], total=total)

@router.get("/{match_id}", response_model=GetMatchResponse) 
async def get_match(match_id: UUID, db: AsyncSession = Depends(get_db)):
    pass 

    result = await db.execute(select(Match).filter(Match.id == match_id))
    match = result.scalar_one_or_none()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    return GetMatchResponse(
        date=match.date.isoformat() if match.date else None, 
        location=match.location,  
        name=match.name,  
        team1Logo=match.team1.logo,
        team1Name=match.team1.name,
        team1Points=match.team1Points,
        team2Logo=match.team2.logo,
        team2Name=match.team2.name,
        team2Points=match.team2Points,
    )

@router.get("/by_team/{team_name}", response_model=MatchListResponse)
async def get_matches_by_team(team_name: str, db: AsyncSession = Depends(get_db)):
    pass 

    result = await db.execute(
        select(Match).filter(
            (Match.team1.ilike(f'%{team_name}%')) | (Match.team2.ilike(f'%{team_name}%'))
        )
    )
    matches = result.scalars().all()
    return MatchListResponse(matches=[MatchResponse(id=match.id) for match in matches], total=len(matches))

@router.get("/by_date/{match_date}", response_model=MatchListResponse)
async def get_matches_by_date(match_date: str, db: AsyncSession = Depends(get_db)):
    pass 

    year, month, day = map(int, match_date.split('-'))
    
    result = await db.execute(
        select(Match).filter(
            extract('year', Match.date) == year,
            extract('month', Match.date) == month,
            extract('day', Match.date) == day
        )
    )
    
    matches = result.scalars().all()
    return MatchListResponse(matches=[MatchResponse(id=match.id) for match in matches], total=len(matches))

@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: UUID, 
    update_request: UpdateMatchRequest, 
    db: AsyncSession = Depends(get_db)
):
    pass 

    result = await db.execute(select(Match).filter(Match.id == match_id))
    match = result.scalar_one_or_none()

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    if update_request.team1Points is not None:
        match.team1Points = update_request.team1Points
    if update_request.team2Points is not None:
        match.team2Points = update_request.team2Points

    await db.commit()
    await db.refresh(match)
    return MatchResponse(id=match.id)
