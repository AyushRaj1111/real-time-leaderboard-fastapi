from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Score(BaseModel):
    user_id: str
    game_id: str
    score: int
