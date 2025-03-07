from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
import redis
import jwt
import bcrypt
from datetime import datetime, timedelta

app = FastAPI()

# JWT settings
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Models
class User(BaseModel):
    username: str
    password: str

class Score(BaseModel):
    user_id: str
    game_id: str
    score: int

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Utility functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = redis_client.hgetall(f"user:{username}")
    if user is None:
        raise credentials_exception
    return user

# User authentication routes
@app.post("/register")
def register(user: User):
    if redis_client.exists(f"user:{user.username}"):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    redis_client.hmset(f"user:{user.username}", {"username": user.username, "password": hashed_password})
    return {"msg": "User registered successfully"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = redis_client.hgetall(f"user:{form_data.username}")
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Score submission routes
@app.post("/submit_score")
def submit_score(score: Score, current_user: User = Depends(get_current_user)):
    redis_client.zadd(f"leaderboard:{score.game_id}", {current_user["username"]: score.score})
    return {"msg": "Score submitted successfully"}

# Leaderboard routes
@app.get("/leaderboard/{game_id}", response_model=List[dict])
def get_leaderboard(game_id: str):
    leaderboard = redis_client.zrevrange(f"leaderboard:{game_id}", 0, -1, withscores=True)
    return [{"username": user, "score": score} for user, score in leaderboard]

@app.get("/ranking/{game_id}/{username}")
def get_ranking(game_id: str, username: str):
    rank = redis_client.zrevrank(f"leaderboard:{game_id}", username)
    if rank is None:
        raise HTTPException(status_code=404, detail="User not found in leaderboard")
    return {"username": username, "rank": rank + 1}

# Top players report routes
@app.get("/top_players/{game_id}/{start_date}/{end_date}", response_model=List[dict])
def get_top_players(game_id: str, start_date: str, end_date: str):
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    top_players = redis_client.zrevrangebyscore(f"leaderboard:{game_id}", end_timestamp, start_timestamp, withscores=True)
    return [{"username": user, "score": score} for user, score in top_players]
