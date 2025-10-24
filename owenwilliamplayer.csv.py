import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_bbr_per_game_stats(season_year):
    """
    Fetch per-game statistics for NBA players for the given season from Basketball-Reference.
    Returns a pandas DataFrame with columns:
      Player, Team, Season, PTS, AST, FG%, TRB, BLK, STL, 3P%, TOV, PF
    """
    # Construct the URL for the per-game stats page for the given season.
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_year}_per_game.html"
    print(f"Fetching season {season_year} from Basketball-Reference: {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the table. On BBR the per-game table has id “per_game_stats” (or similar)
    table = soup.find("table", {"id": "per_game_stats"})
    if table is None:
        raise RuntimeError(f"Could not find per-game stats table for season {season_year}")

    # Use pandas to read the html table (easier)
    df_list = pd.read_html(str(table))
    if not df_list:
        raise RuntimeError(f"No tables found for season {season_year}")
    df = df_list[0]

    # Clean up: drop header repeats, handle players with multiple rows, rename columns
    # Example: drop rows where “Rk” is "Rk" (which are header rows repeated)
    df = df[df["Rk"] != "Rk"].copy()

    # Filter columns we care about and rename
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
    keep_cols = list(rename_map.keys())
    missing = [c for c in keep_cols if c not in df.columns]
    if missing:
        raise RuntimeError(f"Missing columns for season {season_year}: {missing}")

    df2 = df[keep_cols].rename(columns=rename_map)
    df2["Season"] = season_year

    # Convert numeric columns to floats
    numeric_cols = [c for c in df2.columns if c.endswith("_per_game") or c.endswith("_pct")]
    for c in numeric_cols:
        df2[c] = pd.to_numeric(df2[c], errors="coerce")

    return df2

# Example usage for one season
if __name__ == "__main__":
    stats_2023 = get_bbr_per_game_stats(2023)
    print(stats_2023.head())
