from fastapi import APIRouter ,Depends, HTTPException, status
from app.core.database import db_manager
from sqlalchemy.orm import Session
import app.models.users as users
import secrets


router = APIRouter()

@router.post("/games")
async def join_code(db: Session = Depends(db_manager.get_db)):
    try:
        code = secrets.token_hex(3).upper()

        game = users.Game(join_code= code)

        db.add(game)
        db.commit()
        db.refresh(game)

        return {"id": game.id, "join_code": game.join_code}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to write to database"
        )
