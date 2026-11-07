from pydantic import BaseModel, Field

class PlayerCreate(BaseModel):
    join_code: str
    name: str
    is_banker: bool = False
    is_playing: bool = True

class TransferCreate(BaseModel):
    sender_id: int | None
    receiver_id: int | None
    amount: int = Field(gt=0)