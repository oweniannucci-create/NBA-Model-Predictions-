import requests
import pandas as pd

# === 1. NBA schedule JSON feed (official nba.com endpoint) ===
url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json"

# === 2. Get and parse the JSON ===
response = requests.get(url)
data = response.json()

# === 3. Extract and structure the schedule ===
games = []
for day in data["leagueSchedule"]["gameDates"]:
    game_date = day["gameDate"]
    for g in day["games"]:
        game_id = g["gameId"]

        # Skip non-regular-season games (regular season starts with "002")
        if not game_id.startswith("002"):
            continue

        home = g["homeTeam"]
        away = g["awayTeam"]
        venue = g.get("arenaName", "")
        city = g.get("arenaCity", "")
        state = g.get("arenaState", "")

        games.append({
            "date": game_date,
            "game_id": game_id,
            "home_team": home["teamName"],
            "home_team_abbr": home["teamTricode"],
            "away_team": away["teamName"],
            "away_team_abbr": away["teamTricode"],
            "home_score": g.get("homeTeamScore", 0),
            "away_score": g.get("awayTeamScore", 0),
            "status": g["gameStatusText"],
            "arena": venue,
            "city": city,
            "state": state
        })

# === 4. Convert to DataFrame ===
df = pd.DataFrame(games)

# === 5. Format and sort ===
df["date"] = pd.to_datetime(df["date"]).dt.date
df = df.sort_values(by="date").reset_index(drop=True)

# === 6. Save to CSV ===
df.to_csv("nba_2025_26_regular_season_schedule.csv", index=False)

print("✅ Saved full NBA 2025–26 Regular Season schedule as 'nba_2025_26_regular_season_schedule.csv'")
print(df.head(10))
