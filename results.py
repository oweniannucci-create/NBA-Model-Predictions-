from nba_api.stats.endpoints import leaguegamelog
import pandas as pd
from pandasgui import show

nba_team_abbreviations = {
    "ATL": "Hawks",
    "BOS": "Celtics",
    "NJN": "Nets",
    "BRK": "Nets",
    "BKN": "Nets",
    "CHH": "Hornets",
    "CHA": "Hornets",
    "CHI": "Bulls",
    "CLE": "Cavaliers",
    "DAL": "Mavericks",
    "DEN": "Nuggets",
    "DET": "Pistons",
    "GSW": "Warriors",
    "HOU": "Rockets",
    "IND": "Pacers",
    "LAC": "Clippers",
    "LAL": "Lakers",
    "VAN": "Grizzlies",
    "MEM": "Grizzlies",
    "MIA": "Heat",
    "MIL": "Bucks",
    "MIN": "Timberwolves",
    "NOH": "Pelicans",
    "NOP": "Pelicans",
    "NYK": "Knicks",
    "OKC": "Thunder",
    "ORL": "Magic",
    "PHI": "76ers",
    "PHO": "Suns",
    "PHX": "Suns",
    "POR": "Trail Blazers",
    "SAC": "Kings",
    "SAS": "Spurs",
    "TOR": "Raptors",
    "UTA": "Jazz",
    "WAS": "Wizards",
}

# Define the season string for 2025-26
season_id = "2025-26"

# Fetch all regular season games
# SeasonType defaults to 'Regular Season'
game_log = leaguegamelog.LeagueGameLog(
    season=season_id,
    season_type_all_star='Regular Season'
)

# Convert results to a Pandas DataFrame
df = game_log.get_data_frames()[0]

show(df)

# Display basic results: Date, Teams, and Scores
results = df[['GAME_DATE', 'TEAM_ABBREVIATION', 'WL', 'PTS', 'GAME_ID']]
print(f"Retrieved {len(results)} games for the {season_id} season.")
print(results)

results.to_csv(f'nba_results_{season_id}.csv', index=False)
