document.addEventListener("DOMContentLoaded", function() {
    const registerForm = document.getElementById("register-form");
    const loginForm = document.getElementById("login-form");
    const scoreForm = document.getElementById("score-form");

    registerForm.addEventListener("submit", async function(event) {
        event.preventDefault();
        const username = document.getElementById("register-username").value;
        const password = document.getElementById("register-password").value;

        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        alert(data.msg);
    });

    loginForm.addEventListener("submit", async function(event) {
        event.preventDefault();
        const username = document.getElementById("login-username").value;
        const password = document.getElementById("login-password").value;

        const response = await fetch("/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ username, password })
        });

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        alert("Login successful");
    });

    scoreForm.addEventListener("submit", async function(event) {
        event.preventDefault();
        const gameId = document.getElementById("game-id").value;
        const score = document.getElementById("score").value;
        const token = localStorage.getItem("token");

        const response = await fetch("/submit_score", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ game_id: gameId, score })
        });

        const data = await response.json();
        alert(data.msg);
    });

    async function fetchLeaderboard(gameId) {
        const response = await fetch(`/leaderboard/${gameId}`);
        const data = await response.json();
        const leaderboard = document.getElementById("leaderboard");
        leaderboard.innerHTML = data.map(entry => `<div>${entry.username}: ${entry.score}</div>`).join("");
    }

    async function fetchUserRanking(gameId, username) {
        const response = await fetch(`/ranking/${gameId}/${username}`);
        const data = await response.json();
        const userRanking = document.getElementById("user-ranking");
        userRanking.innerHTML = `<div>${data.username}: Rank ${data.rank}</div>`;
    }

    async function fetchTopPlayers(gameId, startDate, endDate) {
        const response = await fetch(`/top_players/${gameId}/${startDate}/${endDate}`);
        const data = await response.json();
        const topPlayers = document.getElementById("top-players");
        topPlayers.innerHTML = data.map(entry => `<div>${entry.username}: ${entry.score}</div>`).join("");
    }

    // Example usage
    fetchLeaderboard("game1");
    fetchUserRanking("game1", "user1");
    fetchTopPlayers("game1", "2022-01-01", "2022-12-31");
});
