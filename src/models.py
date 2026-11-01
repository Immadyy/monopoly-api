from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    join_code: Mapped[str] = mapped_column(unique=True)
    current_round: Mapped[int] = mapped_column(default=1) 
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    name: Mapped[str]
    balance: Mapped[int] = mapped_column(default=25000)
    is_banker: Mapped[bool] = mapped_column(default=False)
    is_playing: Mapped[bool] = mapped_column(default=True)

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    from_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"))
    to_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"))
    amount: Mapped[int]
    type: Mapped[str]
    note: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())