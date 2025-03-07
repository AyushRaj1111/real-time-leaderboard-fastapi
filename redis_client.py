import redis

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Functions to interact with Redis sorted sets for leaderboard storage
def add_score(game_id: str, user_id: str, score: int):
    redis_client.zadd(f"leaderboard:{game_id}", {user_id: score})

def get_leaderboard(game_id: str):
    return redis_client.zrevrange(f"leaderboard:{game_id}", 0, -1, withscores=True)

def get_user_rank(game_id: str, user_id: str):
    return redis_client.zrevrank(f"leaderboard:{game_id}", user_id)

def get_top_players(game_id: str, start_timestamp: int, end_timestamp: int):
    return redis_client.zrevrangebyscore(f"leaderboard:{game_id}", end_timestamp, start_timestamp, withscores=True)
