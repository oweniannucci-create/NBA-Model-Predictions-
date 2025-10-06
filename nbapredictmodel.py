import pandas as pd
from pandasgui import show

df = pd.read_csv("Data/TeamStatistics.csv")

# Convert gameDate to datetime
df['gameDate'] = pd.to_datetime(df['gameDate'])

# Optional: create a season column
# Assuming NBA season starts in October and ends in June
def get_season(date):
    if date.month >= 10:  # October or later
        return f"{date.year}-{date.year+1}"
    else:  # Jan-June
        return f"{date.year-1}-{date.year}"

df['season'] = df['gameDate'].apply(get_season)

# Stats to average
stats = [
    "teamScore",
    "assists",
    "reboundsDefensive",
    "reboundsOffensive",
    "reboundsTotal",
    "steals",
    "blocks",
    "turnovers",
    "foulsPersonal",
    "fieldGoalsMade",
    "fieldGoalsAttempted",
    "fieldGoalsPercentage",
    "threePointersMade",
    "threePointersAttempted",
    "threePointersPercentage",
    "freeThrowsMade",
    "freeThrowsAttempted",
    "freeThrowsPercentage",
    "plusMinusPoints"
]

# Group by season and team
season_team_averages = df.groupby(["season", "teamName"])[stats].mean().reset_index()

# Round for readability
season_team_averages = season_team_averages.round(2)

# Save to CSV
season_team_averages.to_csv("nba_season_team_averages.csv", index=False)

print(season_team_averages)

<<<<<<< HEAD
# Load your full dataset
games_df = pd.read_csv("Data/Games.csv")

# Filter for one specific season, for example 2024-25
games_df["gameDate"] = pd.to_datetime(games_df["gameDate"])

# Filter for a specific year, e.g., 2024
year = 2024
season_games = games_df[games_df["gameDate"].dt.year == year].copy()

# Calculate the team averages *just for that season*
team_avg_df = (
    season_games
    .groupby("teamName")
    .mean(numeric_only=True)
    .reset_index()
)

# Optional: rename columns to make clear these are averages
team_avg_df = team_avg_df.add_suffix("_avg")
team_avg_df = team_avg_df.rename(columns={"teamName_avg": "teamName"})

# Merge the averages back into the season's games
merged_df = season_games.merge(team_avg_df, on="teamName", how="left")

print(merged_df.head())

merged_df = (
    season_games
    .merge(team_avg_df, on="teamName", how="left", suffixes=("", "_teamAvg"))
    .merge(team_avg_df, left_on="opponentTeamName", right_on="teamName", how="left", suffixes=("", "_oppAvg"))
)




=======
show(season_team_averages)
>>>>>>> b30bd5213ca1699542ee41e67c69062cbc725734


