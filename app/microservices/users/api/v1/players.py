from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.microservices.users.schemas.player import Player, PlayerCreate, PlayerDelete, PlayerList, PlayerUpdate
from app.microservices.users.utils.db import get_db
from app.microservices.users.models.player import player_matches_association, player_teams_association

router = APIRouter(
    prefix="/players",
    tags=["players"]
)

@router.post("/", response_model=Player, status_code=201)
async def create_player(player: PlayerCreate, db: AsyncSession = Depends(get_db)):
    db_player = Player(**player.dict())
    db.add(db_player)
    await db.commit()
    await db.refresh(db_player)
    return db_player

@router.get("/{player_id}", response_model=Player)
async def get_player(player_id: UUID, db: AsyncSession = Depends(get_db)):
    player = await db.execute(select(Player).filter(Player.id == player_id))
    player = player.scalars().first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.put("/{player_id}", status_code=204)
async def update_player(player_id: UUID, player_update: PlayerUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Player).filter(Player.id == player_id))
    player = result.scalars().first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    for key, value in player_update.dict(exclude_unset=True).items():
        setattr(player, key, value)
    await db.commit()
    return

@router.delete("/{player_id}", status_code=204)
async def delete_player(player_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Player).filter(Player.id == player_id))
    player = result.scalars().first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    await db.delete(player)
    await db.commit()
    return  

@router.get("/", response_model=PlayerList)
async def list_players(
    name: Optional[str] = Query(None, description="Search players by name (substring search)"),
    team_id: Optional[UUID] = Query(None, description="Filter by team ID"),
    role: Optional[str] = Query(None, description="Filter by player role"),
    match_id: Optional[UUID] = Query(None, description="Filter by match ID"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    query = db.query(Player)
    
    if name:
        query = query.filter(Player.full_name.ilike(f"%{name}%"))
    if team_id:
        query = query.filter(Player.team_id == team_id)
    if role:
        query = query.filter(Player.role == role)
    if match_id:
        query = query.join(player_matches_association).filter(player_matches_association.c.match_id == match_id)

    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    players = await db.execute(query.offset((page - 1) * size).limit(size))
    players = players.scalars().all()

    return PlayerList(players=players, total=total, page=page, size=size)

@router.get("/team/{team_id}", response_model=PlayerList)
async def get_players_by_team(team_id: UUID, db: AsyncSession = Depends(get_db)):
    players = await db.execute(select(Player).filter(Player.team_id == team_id))
    players = players.scalars().all()
    return PlayerList(players=players, total=len(players), page=1, size=len(players))

@router.get("/role/{role}", response_model=PlayerList)
async def get_players_by_role(role: str, db: AsyncSession = Depends(get_db)):
    players = await db.execute(select(Player).filter(Player.role == role))
    players = players.scalars().all()
    return PlayerList(players=players, total=len(players), page=1, size=len(players))

@router.get("/match/{match_id}", response_model=PlayerList)
async def get_players_by_match(match_id: UUID, db: AsyncSession = Depends(get_db)):
    players = await db.execute(
        select(Player)
        .join(player_matches_association)
        .filter(player_matches_association.c.match_id == match_id)
    )
    players = players.scalars().all()
    return PlayerList(players=players, total=len(players), page=1, size=len(players))

@router.post("/{player_id}/matches/{match_id}", status_code=204)
async def add_match_to_player(player_id: UUID, match_id: UUID, db: AsyncSession = Depends(get_db)):
    player = await db.execute(select(Player).filter(Player.id == player_id))
    player = player.scalars().first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    await db.execute(
        player_matches_association.insert().values(player_id=player_id, match_id=match_id)
    )
    await db.commit()
    return

@router.post("/{player_id}/teams/{team_id}", status_code=204)
async def add_team_to_player(player_id: UUID, team_id: UUID, db: AsyncSession = Depends(get_db)):
    player = await db.execute(select(Player).filter(Player.id == player_id))
    player = player.scalars().first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    await db.execute(
        player_teams_association.insert().values(player_id=player_id, team_id=team_id)
    )
    await db.commit()
    return  
