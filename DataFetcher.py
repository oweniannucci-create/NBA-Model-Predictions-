from nba_api.stats.endpoints import DraftHistory
import pandas as pd
#from pandasgui import show


def get_average_draft_data():

    draft_data = DraftHistory().get_data_frames()[0]

    df = draft_data[['TEAM_CITY', 'TEAM_NAME', 'season', 'OVERALL_PICK']].copy()
    df['team_name'] = df['TEAM_CITY'] + ' ' + df['TEAM_NAME']


    summary_df = (
        df.groupby(['team_name', 'season'])
        .agg(
            number_of_picks=('OVERALL_PICK', 'count'),
            average_overall_pick=('OVERALL_PICK', 'mean')
        )
        .reset_index()
        .sort_values(['team_name', 'season'], ascending=[True, False])
    )

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    pd.set_option('display.colheader_justify', 'center')

    #print(summary_df)
    #show(summary_df)

    return summary_df


def get_cleaned_games_with_winner_column():
    # Load your dataset
    df = pd.read_csv("Data/Games.csv")

    # Drop the columns you don't need
    columns_to_drop = ["arenaId", "homeTeamCity", "awayTeamCity","seriesgamenumber","gamelabel","gamesublabel","attendance","homescore","awayscore","gameid","hometeamcity"]
    df = df.drop(columns=columns_to_drop, errors="ignore")

    # Define a function to assign a season based on the game date
    def assign_season(date_str):
        # Make sure the date is parsed properly
        date = pd.to_datetime(date_str)
        year = date.year
        # NBA seasons start in the fall of one year and end in the next
        if date.month >= 10:  # October or later → start of a new season
            return f"{year}-{year + 1}"
        else:  # January to June → still part of the previous season
            return f"{year - 1}-{year}"

    # Apply the season function to create a new column
    df["season"] = df["gameDate"].apply(assign_season)

    # Save the cleaned version to a new file
    df.to_csv("games_cleaned.csv", index=False)

    #print("Columns dropped and 'season' column added successfully!")
    #print(df.head())


    # Standardize column names just in case (lowercase all)
    df.columns = df.columns.str.lower()

    # Convert winner column into 1 (home team) or 0 (away team)
    df["winner_binary"] = df.apply(
        lambda row: 1 if row["winner"] == row["hometeamid"] else 0, axis=1
    )

    # (Optional) drop the original winner column
    # df = df.drop(columns=["winner"])

    # Save the updated CSV
    df.to_csv("games_with_winner_binary.csv", index=False)

    #print("Converted 'winner' column to binary (1 = home win, 0 = away win).")
    #print(df[["hometeamname", "awayteamname", "winner", "winner_binary"]].head())

    #show (df)

    #print (df.info())
    return df


def get_teamaveragestatistics_from_year():

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

    #print(season_team_averages)




    return season_team_averages
    return season_team_averages