from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import db_manager
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
import app.models.users as users
from app.schemas.users import PlayerCreate 
import secrets
import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter()

@router.post("/games")
def create_game(db: Session = Depends(db_manager.get_db)):
    try:
        code = secrets.token_hex(3).upper()
        game = users.Game(join_code=code)

        db.add(game)
        db.commit()
        db.refresh(game)

        return {"id": game.id, "join_code": game.join_code}

    except SQLAlchemyError as e:
        db.rollback()

        logger.error(f"Failed to create game in database: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to initialize a new game session. Please try again."
        )


@router.post("/players")
def add_player(data: PlayerCreate, db: Session = Depends(db_manager.get_db)):
    # 1. Verify the game session exists
    game = db.scalars(select(users.Game).where(users.Game.join_code == data.join_code.upper())).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Game session with code '{data.join_code}' was not found."
        )

    # 2. Prevent duplicate names within this specific game
    existing_player = db.scalars(
        select(users.Player).where(
            and_(
                users.Player.game_id == game.id,
                users.Player.name == data.name
            )
        )
    ).first()

    if existing_player:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"The name '{data.name}' is already taken in this game session."
        )

    # 3. Everything is safe; execute database transaction
    try:
        player = users.Player(
            game_id=game.id, 
            name=data.name, 
            is_banker=data.is_banker, 
            is_playing=data.is_playing
        )
        
        db.add(player)
        db.commit()
        db.refresh(player)
        
        return {
            "id": player.id, 
            "name": player.name, 
            "balance": player.balance, 
            "is_banker": player.is_banker, 
            "is_playing": player.is_playing
        }

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to add player '{data.name}' to game {game.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="An unexpected error occurred while joining the game."
        )