# import pandas as pd
# from pandasgui import show
#
# df = pd.read_csv("Data/TeamStatistics.csv")
#
# # Convert gameDate to datetime
# df['gameDate'] = pd.to_datetime(df['gameDate'])
#
# # Optional: create a season column
# # Assuming NBA season starts in October and ends in June
# def get_season(date):
#     if date.month >= 10:  # October or later
#         return f"{date.year}-{date.year+1}"
#     else:  # Jan-June
#         return f"{date.year-1}-{date.year}"
#
# df['season'] = df['gameDate'].apply(get_season)
#
# # Stats to average
# stats = [
#     "teamScore",
#     "assists",
#     "reboundsDefensive",
#     "reboundsOffensive",
#     "reboundsTotal",
#     "steals",
#     "blocks",
#     "turnovers",
#     "foulsPersonal",
#     "fieldGoalsMade",
#     "fieldGoalsAttempted",
#     "fieldGoalsPercentage",
#     "threePointersMade",
#     "threePointersAttempted",
#     "threePointersPercentage",
#     "freeThrowsMade",
#     "freeThrowsAttempted",
#     "freeThrowsPercentage",
#     "plusMinusPoints"
# ]
#
# # Group by season and team
# season_team_averages = df.groupby(["season", "teamName"])[stats].mean().reset_index()
#
# # Round for readability
# season_team_averages = season_team_averages.round(2)
#
# # Save to CSV
# season_team_averages.to_csv("nba_season_team_averages.csv", index=False)
#
# print(season_team_averages)
#
# show(season_team_averages)

from nba_api.stats.endpoints import DraftHistory
import pandas as pd

# Get the full draft history
all_draft = DraftHistory().get_data_frames()[0]

# Select relevant columns
df = all_draft[['PLAYER_NAME', 'SEASON', 'ROUND_NUMBER', 'OVERALL_PICK', 'TEAM_NAME']]

# Optional: sort by season, round, and pick
df = df.sort_values(['SEASON', 'ROUND_NUMBER', 'OVERALL_PICK'])

# Make sure pandas shows all rows
pd.set_option('display.max_rows', None)

# Print the full draft table
print(df)

# Count how many draft picks each team has made
team_pick_counts = df['TEAM_NAME'].value_counts()

print(team_pick_counts)
# Count how many draft picks each team has made
team_pick_counts = df['TEAM_NAME'].value_counts()

print(team_pick_counts)
unique_teams = df['TEAM_NAME'].dropna().unique()

for team in sorted(unique_teams):
    team_draft = df[df['TEAM_NAME'] == team]
    print(f"\n=== {team} ({len(team_draft)} picks) ===")
    print(team_draft[['SEASON', 'PLAYER_NAME', 'ROUND_NUMBER', 'OVERALL_PICK']])

