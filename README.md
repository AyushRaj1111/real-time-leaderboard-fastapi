# Real-Time Leaderboard with FastAPI

This project is a real-time leaderboard application built with FastAPI and Redis. It allows users to register, log in, submit scores, and view leaderboards for different games.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AyushRaj1111/real-time-leaderboard-fastapi.git
   cd real-time-leaderboard-fastapi
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

5. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the API documentation.

## Usage

### Register a new user
Send a POST request to `/register` with the following JSON body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

### Log in
Send a POST request to `/token` with the following form data:
- `username`: your_username
- `password`: your_password

The response will contain an access token that you can use to authenticate subsequent requests.

### Submit a score
Send a POST request to `/submit_score` with the following JSON body:
```json
{
  "game_id": "game1",
  "score": 100
}
```
Include the access token in the `Authorization` header:
```
Authorization: Bearer your_access_token
```

### View the global leaderboard
Send a GET request to `/leaderboard/{game_id}` to retrieve the leaderboard for a specific game.

### View user ranking
Send a GET request to `/ranking/{game_id}/{username}` to retrieve the ranking of a specific user in a specific game.

### View top players report
Send a GET request to `/top_players/{game_id}/{start_date}/{end_date}` to retrieve the top players for a specific game within a date range.

## API Endpoints

- `POST /register`: Register a new user
- `POST /token`: Log in and obtain an access token
- `POST /submit_score`: Submit a score for a specific game
- `GET /leaderboard/{game_id}`: Retrieve the global leaderboard for a specific game
- `GET /ranking/{game_id}/{username}`: Retrieve the ranking of a specific user in a specific game
- `GET /top_players/{game_id}/{start_date}/{end_date}`: Retrieve the top players for a specific game within a date range

## Contribution Guidelines

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch to your fork.
4. Create a pull request with a detailed description of your changes.

We welcome contributions from the community to improve this project!
