import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_bbr_per_game_stats(season_year):
    """
    Fetch per-game statistics for NBA players for the given season from Basketball-Reference.
    Returns a pandas DataFrame with columns:
      Player, Team, Season, PTS_per_game, AST_per_game, FG_pct, TRB_per_game,
      BLK_per_game, STL_per_game, 3P_pct, TOV_per_game, PF_per_game
    """
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_year}_per_game.html"
    print(f"Fetching season {season_year} from Basketball-Reference: {url}")

    # Download the webpage
    resp = requests.get(url)
    resp.raise_for_status()

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the per-game stats table
    table = soup.find("table", {"id": "per_game_stats"})
    if table is None:
        raise RuntimeError(f"❌ Could not find per-game stats table for season {season_year}")

    # Read table directly with pandas
    df_list = pd.read_html(str(table))
    if not df_list:
        raise RuntimeError(f"❌ No tables found for season {season_year}")
    df = df_list[0]

    # Remove duplicate header rows
    df = df[df["Rk"] != "Rk"].copy()

    # Drop rows with missing player names
    df = df.dropna(subset=["Player"])

    # Handle players who played for multiple teams:
    # BBR has a "TOT" row summarizing total season stats — keep that and drop duplicates.
    df = df.drop_duplicates(subset=["Player", "Tm"], keep="first")
    df = df[df["Tm"] != "TOT"].append(df[df["Tm"] == "TOT"], ignore_index=True)

    # Filter and rename columns
    rename_map = {
        "Player": "Player",
        "Tm": "Team",
        "PTS": "PTS_per_game",
        "AST": "AST_per_game",
        "FG%": "FG_pct",
        "TRB": "TRB_per_game",
        "BLK": "BLK_per_game",
        "STL": "STL_per_game",
        "3P%": "3P_pct",
        "TOV": "TOV_per_game",
        "PF": "PF_per_game"
    }

    keep_cols = [c for c in rename_map.keys() if c in df.columns]
    df2 = df[keep_cols].rename(columns=rename_map)

    # Add Season column (formatted like 2022-23)
    df2["Season"] = f"{season_year - 1}-{str(season_year)[-2:]}"

    # Convert numeric columns
    numeric_cols = [c for c in df2.columns if c.endswith("_per_game") or c.endswith("_pct")]
    df2[numeric_cols] = df2[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Reset index for cleanliness
    df2.reset_index(drop=True, inplace=True)

    return df2


# Example usage
if __name__ == "__main__":
    stats_2023 = get_bbr_per_game_stats(2023)
    print(stats_2023.head())
