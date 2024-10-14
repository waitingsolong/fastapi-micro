from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from app.microservices.users.models.fan import Fan
from app.microservices.users.utils.db import get_db
from app.microservices.users.schemas.fan import FanCreate, FanListResponse, FanResponse, FanUpdate

router = APIRouter(
    prefix="/fans",
    tags=["fans"]
)

@router.post("/", response_model=FanResponse, status_code=status.HTTP_201_CREATED)
async def create_fan(fan: FanCreate, db: AsyncSession = Depends(get_db)):
    new_fan = Fan(**fan.model_dump())
    db.add(new_fan)
    await db.commit()
    await db.refresh(new_fan)
    return new_fan


@router.get("/{fan_id}", response_model=FanResponse)
async def get_fan(fan_id: UUID4, db: AsyncSession = Depends(get_db)):
    fan = await db.get(Fan, fan_id)
    if fan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fan not found")
    return fan


@router.put("/{fan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_fan(fan_id: UUID4, fan: FanUpdate, db: AsyncSession = Depends(get_db)):
    db_fan = await db.get(Fan, fan_id)
    if db_fan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fan not found")
    
    for key, value in fan.model_dump(exclude_unset=True).items():
        setattr(db_fan, key, value)
    
    await db.commit()
    return


@router.delete("/{fan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fan(fan_id: UUID4, db: AsyncSession = Depends(get_db)):
    fan = await db.get(Fan, fan_id)
    if fan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fan not found")
    
    await db.delete(fan)
    await db.commit()
    return


@router.get("/", response_model=FanListResponse)
async def list_fans(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    query = await db.execute(f"SELECT * FROM fans OFFSET {skip} LIMIT {limit}")
    fans = query.fetchall()
    total = await db.execute("SELECT COUNT(*) FROM fans")
    return {"fans": fans, "total": total.scalar()}


# TODO crud
# favourite players
@router.post("/favourite_players/", status_code=status.HTTP_204_NO_CONTENT)
async def add_favourite_player(fan_id: UUID4, player_id: UUID4, db: AsyncSession = Depends(get_db)):
    fan = await db.get(Fan, fan_id)
    if fan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fan not found")
    
    if not fan.add_favourite_player(player_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Max limit reached")
    
    await db.commit()
    return


# TODO crud
# favourite matches 
@router.post("/favourite_matches/", status_code=status.HTTP_204_NO_CONTENT)
async def add_favourite_match(fan_id: UUID4, match_id: UUID4, db: AsyncSession = Depends(get_db)):
    fan = await db.get(Fan, fan_id)
    if fan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fan not found")
    
    if not fan.add_favourite_match(match_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Max limit reached")
    
    await db.commit()
    return


# TODO crud
# favourite teams
@router.post("/favourite_teams/", status_code=status.HTTP_204_NO_CONTENT)
async def add_favourite_team(fan_id: UUID4, team_id: UUID4, db: AsyncSession = Depends(get_db)):
    fan = await db.get(Fan, fan_id)
    if fan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fan not found")
    
    if not fan.add_favourite_team(team_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Max limit reached")
    
    await db.commit()
    return
