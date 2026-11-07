from pydantic import BaseModel

class PlayerCreate(BaseModel):
    join_code: str
    name: str
    is_banker: bool = False
    is_playing: bool = True