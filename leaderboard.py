from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import redis
from datetime import datetime

router = APIRouter()

# Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Models
class Score(BaseModel):
    user_id: str
    game_id: str
    score: int

# Score submission endpoint
@router.post("/submit_score")
def submit_score(score: Score):
    redis_client.zadd(f"leaderboard:{score.game_id}", {score.user_id: score.score})
    return {"msg": "Score submitted successfully"}

# Global leaderboard endpoint
@router.get("/leaderboard/{game_id}", response_model=List[dict])
def get_leaderboard(game_id: str):
    leaderboard = redis_client.zrevrange(f"leaderboard:{game_id}", 0, -1, withscores=True)
    return [{"user_id": user, "score": score} for user, score in leaderboard]

# User ranking endpoint
@router.get("/ranking/{game_id}/{user_id}")
def get_ranking(game_id: str, user_id: str):
    rank = redis_client.zrevrank(f"leaderboard:{game_id}", user_id)
    if rank is None:
        raise HTTPException(status_code=404, detail="User not found in leaderboard")
    return {"user_id": user_id, "rank": rank + 1}

# Top players report generation endpoint
@router.get("/top_players/{game_id}/{start_date}/{end_date}", response_model=List[dict])
def get_top_players(game_id: str, start_date: str, end_date: str):
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    top_players = redis_client.zrevrangebyscore(f"leaderboard:{game_id}", end_timestamp, start_timestamp, withscores=True)
    return [{"user_id": user, "score": score} for user, score in top_players]
