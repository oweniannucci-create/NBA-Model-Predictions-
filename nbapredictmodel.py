def get_teamaveragestatistics_from_year():
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


    # Load your full dataset
    games_df = pd.read_csv("Data/Games.csv")



    # Merge the averages back into the season's games
    # #merged_df = games_df.merge(
    #     season_team_averages,
    #     left_on="hometeamName",
    #     right_on="teamName",
    #     how="left"

    #show(merged_df)





    show(season_team_averages)
    return season_team_averages


