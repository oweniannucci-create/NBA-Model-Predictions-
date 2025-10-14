# import pandas as pd
from pandasgui import show
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

# all_draft = DraftHistory().get_data_frames()[0]
#
# df = all_draft[['PLAYER_NAME', 'SEASON', 'ROUND_NUMBER', 'OVERALL_PICK', 'TEAM_NAME']]
#
# df = df.sort_values(['SEASON', 'ROUND_NUMBER', 'OVERALL_PICK'])
#
# pd.set_option('display.max_rows', None)
#
# team_pick_counts = df['TEAM_NAME'].value_counts()
#
# print(team_pick_counts)
# team_pick_counts = df['TEAM_NAME'].value_counts()
#
# print(team_pick_counts)
# unique_teams = df['TEAM_NAME'].dropna().unique()
#
# for team in sorted(unique_teams):
#     team_draft = df[df['TEAM_NAME'] == team]
#     print(f"\n=== {team} ({len(team_draft)} picks) ===")
#     print(team_draft[['SEASON', 'PLAYER_NAME', 'ROUND_NUMBER', 'OVERALL_PICK']])
#
# team_round_counts = df.groupby(['TEAM_NAME', 'ROUND_NUMBER']).size().unstack(fill_value=0)
#
# team_round_counts['Total'] = team_round_counts.sum(axis=1)
#
# team_round_counts = team_round_counts.sort_values('Total', ascending=False)
#
# print(team_round_counts.to_string())

# import matplotlib.pyplot as plt
#
# round_data = team_round_counts.drop(columns=['Total'])
#
# top_10 = round_data.loc[team_round_counts['Total'].nlargest(10).index]
#
# ax = top_10.plot(kind='bar', stacked=True, figsize=(12, 7), colormap='tab20')
#
# plt.title('NBA Draft Picks by Team and Round (Top 10 Teams)')
# plt.xlabel('Team')
# plt.ylabel('Number of Draft Picks')
# plt.legend(title='Draft Round', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()

# def team_pick_counts (team):bn
#     team_pick_counts = df[df['TEAM_NAME'] == team]
#
# print(team_pick_counts('Bulls'))

import pandas as pd
from nba_api.stats.endpoints import DraftHistory

def get_average_draft_data():

    draft_data = DraftHistory().get_data_frames()[0]

    df = draft_data[['TEAM_CITY', 'TEAM_NAME', 'SEASON', 'OVERALL_PICK']].copy()
    df['team_name'] = df['TEAM_CITY'] + ' ' + df['TEAM_NAME']
    df['draft_year'] = df['SEASON']


    summary_df = (
        df.groupby(['team_name', 'draft_year'])
        .agg(
            number_of_picks=('OVERALL_PICK', 'count'),
            average_overall_pick=('OVERALL_PICK', 'mean')
        )
        .reset_index()
        .sort_values(['team_name', 'draft_year'], ascending=[True, False])
    )

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    pd.set_option('display.colheader_justify', 'center')

    print(summary_df)
    show(summary_df)

    return summary_df

get_average_draft_data()