from fastapi import APIRouter, Depends, HTTPException, status
import secrets, logging

from app.core.database import db_manager

from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError

import app.models.users as users

from app.schemas.users import PlayerCreate, TransferCreate


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


@router.post("/transfer")
def make_transfer(data: TransferCreate, db: Session = Depends(db_manager.get_db)):

    if data.sender_id is None and data.receiver_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="atleast one player must have ID"
        )

    sen = db.get(users.Player, data.sender_id) if data.sender_id is not None else None
    rec = db.get(users.Player, data.receiver_id) if data.receiver_id is not None else None

    if data.sender_id is not None and not sen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {data.sender_id} not found",
        )

    if data.receiver_id is not None and not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {data.receiver_id} not found",
        )


    sender_name = sen.name if sen is not None else None
    receiver_name = rec.name if rec is not None else None

    return {
        "sender_id": sender_name,
        "receiver_id": receiver_name
    }
