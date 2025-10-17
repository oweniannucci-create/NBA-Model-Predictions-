import DataFetcher


games_df = DataFetcher.get_cleaned_games_with_winner_column()
stats_df = DataFetcher.get_teamaveragestatistics_from_year()
draft_df = DataFetcher.get_average_draft_data()

print(games_df.info())
print(stats_df.info())
print(draft_df.info())

from nba_api.stats.endpoints import DraftHistory
import pandas as pd

def get_average_draft_data():
    draft_data = DraftHistory().get_data_frames()[0]

    df = draft_data[['TEAM_CITY', 'TEAM_NAME', 'SEASON', 'OVERALL_PICK']].copy()
    df['team_name'] = df['TEAM_CITY'] + ' ' + df['TEAM_NAME']
    df['season'] = df['SEASON'].astype(str)

    summary_df = (
        df.groupby(['team_name', 'season'])
        .agg(
            number_of_picks=('OVERALL_PICK', 'count'),
            average_overall_pick=('OVERALL_PICK', 'mean')
        )
        .reset_index()
    )

    return summary_df


def get_cleaned_games_with_winner_column():
    df = pd.read_csv("Data/Games.csv")

    # Drop unnecessary columns
    columns_to_drop = ["arenaId", "homeTeamCity", "awayTeamCity","seriesgamenumber","gamelabel","gamesublabel","attendance","homescore","awayscore","gameid","hometeamcity","gametype"]
    df = df.drop(columns=columns_to_drop, errors="ignore")

    # Assign NBA season based on date
    def assign_season(date_str):
        date = pd.to_datetime(date_str)
        year = date.year
        return f"{year}-{year+1}" if date.month >= 10 else f"{year-1}-{year}"

    df["season"] = df["gameDate"].apply(assign_season)
    df.columns = df.columns.str.lower()

    # Create winner binary column (1 = home win, 0 = away win)
    df["winner_binary"] = df.apply(lambda row: 1 if row["winner"] == row["hometeamid"] else 0, axis=1)

    return df


def get_teamaveragestatistics_from_year():
    df = pd.read_csv("Data/TeamStatistics.csv")

    df['gameDate'] = pd.to_datetime(df['gameDate'])

    def get_season(date):
        return f"{date.year}-{date.year+1}" if date.month >= 10 else f"{date.year-1}-{date.year}"

    df['season'] = df['gameDate'].apply(get_season)

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

    season_team_averages = df.groupby(["season", "teamName"])[stats].mean().reset_index()
    season_team_averages = season_team_averages.round(2)

    return season_team_averages


def combine_game_team_draft_data():
    # Load all data
    games_df = get_cleaned_games_with_winner_column()
    team_stats_df = get_teamaveragestatistics_from_year()
    draft_df = get_average_draft_data()

    # Prepare season column for previous season lookup
    def previous_season(season):
        start, end = map(int, season.split('-'))
        return f"{start-1}-{end-1}"

    games_df["prev_season"] = games_df["season"].apply(previous_season)

    # Merge team averages (home and away) from previous season
    merged = games_df.merge(
        team_stats_df,
        left_on=["prev_season", "hometeamname"],
        right_on=["season", "teamName"],
        how="left",
        suffixes=("", "_home")
    ).merge(
        team_stats_df,
        left_on=["prev_season", "awayteamname"],
        right_on=["season", "teamName"],
        how="left",
        suffixes=("_home", "_away")
    )

    # Merge draft data (home and away) from previous season
    merged = merged.merge(
        draft_df,
        left_on=["prev_season", "hometeamname"],
        right_on=["season", "team_name"],
        how="left"
    ).rename(columns={
        "number_of_picks": "home_number_of_picks",
        "average_overall_pick": "home_avg_overall_pick"
    }).drop(columns=["team_name", "season"])

    merged = merged.merge(
        draft_df,
        left_on=["prev_season", "awayteamname"],
        right_on=["season", "team_name"],
        how="left"
    ).rename(columns={
        "number_of_picks": "away_number_of_picks",
        "average_overall_pick": "away_avg_overall_pick"
    }).drop(columns=["team_name", "season"])

    # Save final merged dataset
    merged.to_csv("combined_games_team_draft.csv", index=False)

    print("✅ Combined dataset created: combined_games_team_draft.csv")
    print("Columns:", merged.columns.tolist())
    return merged


# Run it
if __name__ == "__main__":
    final_df = combine_game_team_draft_data()
    print(final_df.head())
