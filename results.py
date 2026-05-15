from nba_api.stats.endpoints import leaguegamelog
import pandas as pd


import pandas as pd
from nba_api.stats.endpoints import leaguegamelog

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

season_id = "2025-26"

# Fetch regular season games
game_log = leaguegamelog.LeagueGameLog(
    season=season_id, season_type_all_star="Regular Season"
)
df = game_log.get_data_frames()[0]

# Identify home teams (MATCHUP column has ' vs. ') and map mascots
df["IS_HOME"] = df["MATCHUP"].str.contains(" vs. ")
df["MASCOT"] = df["TEAM_ABBREVIATION"].map(nba_team_abbreviations)

# Split into home and away dataframes
home_df = df[df["IS_HOME"]][["GAME_ID", "GAME_DATE", "MASCOT", "WL"]].copy()
away_df = df[~df["IS_HOME"]][["GAME_ID", "MASCOT"]].copy()

# Rename columns to merge into single game rows
home_df = home_df.rename(columns={"MASCOT": "HOME_TEAM", "WL": "HOME_RESULT"})
away_df = away_df.rename(columns={"MASCOT": "AWAY_TEAM"})

# Combine into a single matchup DataFrame
combined_df = pd.merge(home_df, away_df, on="GAME_ID")

# Create 1 (Home Win) or 0 (Home Loss)
combined_df["HOME_WIN"] = combined_df["HOME_RESULT"].apply(
    lambda x: 1 if x == "W" else 0
)

# FIXED HERE: Use 'GAME_DATE' because it came from home_df, then use .rename() right away
final_results = combined_df[
    ["GAME_DATE", "HOME_TEAM", "AWAY_TEAM", "HOME_WIN", "GAME_ID"]
].reset_index(drop=True)
final_results = final_results.rename(columns={"GAME_DATE": "gamedate"})

print(f"Retrieved {len(final_results)} matchups for the {season_id} season.")
print(final_results.head())

# Save to CSV (The CSV will now show 'gamedate' as the column header)
final_results.to_csv(f"nba_home_away_results_{season_id}.csv", index=False)









# nba_team_abbreviations = {
#     "ATL": "Hawks", "BOS": "Celtics", "NJN": "Nets", "BRK": "Nets", "BKN": "Nets",
#     "CHH": "Hornets", "CHA": "Hornets", "CHI": "Bulls", "CLE": "Cavaliers",
#     "DAL": "Mavericks", "DEN": "Nuggets", "DET": "Pistons", "GSW": "Warriors",
#     "HOU": "Rockets", "IND": "Pacers", "LAC": "Clippers", "LAL": "Lakers",
#     "VAN": "Grizzlies", "MEM": "Grizzlies", "MIA": "Heat", "MIL": "Bucks",
#     "MIN": "Timberwolves", "NOH": "Pelicans", "NOP": "Pelicans", "NYK": "Knicks",
#     "OKC": "Thunder", "ORL": "Magic", "PHI": "76ers", "PHO": "Suns",
#     "PHX": "Suns", "POR": "Trail Blazers", "SAC": "Kings", "SAS": "Spurs",
#     "TOR": "Raptors", "UTA": "Jazz", "WAS": "Wizards",
# }
#
# season_id = "2025-26"
#
# # Fetch regular season games
# game_log = leaguegamelog.LeagueGameLog(
#     season=season_id,
#     season_type_all_star='Regular Season'
# )
#
# df = game_log.get_data_frames()[0]
#
# # Identify home teams (MATCHUP column has ' vs. ') and map mascots
# df['IS_HOME'] = df['MATCHUP'].str.contains(' vs. ')
# df['MASCOT'] = df['TEAM_ABBREVIATION'].map(nba_team_abbreviations)
#
# # Split into home and away dataframes
# home_df = df[df['IS_HOME']][['GAME_ID', 'GAME_DATE', 'MASCOT', 'WL']].copy()
# away_df = df[~df['IS_HOME']][['GAME_ID', 'MASCOT']].copy()
# df = df.rename(columns={"GAME_DATE": "gamedate"})
# # Rename columns to merge into single game rows
# home_df = home_df.rename(columns={'MASCOT': 'HOME_TEAM', 'WL': 'HOME_RESULT'})
# away_df = away_df.rename(columns={'MASCOT': 'AWAY_TEAM'})
# # gamedate_df = gamedate_df.rename(columns={'GAME_DATE': 'gamedate'})
#
# # Combine into a single matchup DataFrame
# combined_df = pd.merge(home_df, away_df, on='GAME_ID')
#
# # Create 1 (Home Win) or 0 (Home Loss)
# combined_df['HOME_WIN'] = combined_df['HOME_RESULT'].apply(lambda x: 1 if x == 'W' else 0)
#
# # Clean up and organize the final dataset
# final_results = combined_df[['GAME_DATE', 'HOME_TEAM', 'AWAY_TEAM', 'HOME_WIN', 'GAME_ID']].reset_index(drop=True)
#
# print(f"Retrieved {len(final_results)} matchups for the {season_id} season.")
# print(final_results.head())
#
# # Save to CSV
# final_results.to_csv(f'nba_home_away_results_{season_id}.csv', index=False)



