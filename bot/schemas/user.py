from pydantic import BaseModel

class User(BaseModel):
    game_is_active: bool = False
