import pandas as pd
from nba_api.stats.endpoints import scheduleleaguev2

try:
    from pandasgui import show
except ImportError:
    show = None


def get_full_schedule(season="2025-26"):
    """
    Pulls the full NBA schedule for the specified season using ScheduleLeagueV2.
    Returns a cleaned DataFrame with past and upcoming games.
    """
    print(f"Fetching NBA schedule for the {season} season...")
    sched = scheduleleaguev2.ScheduleLeagueV2(season=season)
    games = sched.get_data_frames()[0]

    # Debug info – helpful if NBA API schema changes again
    print("Columns returned by NBA API:", list(games.columns))

    # The correct date column is 'gameDate'
    date_col = "gameDate"

    rename_map = {
        date_col: "game_date",
        "gameId": "game_id",
        "gameStatusText": "status_text",
        "homeTeam_teamCity": "hometeamcity",
        "homeTeam_teamName": "hometeamname",
        "awayTeam_teamCity": "awayteamcity",
        "awayTeam_teamName": "awayteamname",
    }

    df = games.rename(columns=rename_map)

    # Convert date and sort
    df["game_date"] = pd.to_datetime(df["game_date"], errors="coerce")
    df = df.dropna(subset=["game_date"])
    df = df.sort_values("game_date").reset_index(drop=True)

    # Add a played flag
    df["played"] = df["status_text"].str.lower().isin(["final", "completed", "ended"])

    # Add season info
    df["season"] = season

    # ✅ Corrected columns to keep
    keep_cols = [
        "season",
        "game_id",
        "game_date",
        "hometeamcity",
        "hometeamname",
        "awayteamcity",
        "awayteamname",
        "status_text",
        "played"
    ]

    # Only keep those that exist
    df = df[[c for c in keep_cols if c in df.columns]]

    return df


def save_schedule_to_csv(season="2025-26", output_file="nba_schedule_2025_26.csv"):
    """
    Fetches and saves the full NBA schedule for the specified season.
    """
    df = get_full_schedule(season)
    df.to_csv(output_file, index=False)
    print(f"✅ Schedule for the {season} season saved to {output_file}")
    return df


if __name__ == "__main__":
    df = save_schedule_to_csv("2025-26")

    print(f"\n📅 Displaying the {df['season'].iloc[0]} NBA schedule:")
    print(df.head(10))

    if show:
        show(df)
