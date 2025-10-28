import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandasgui import show

# --------------------------
# Function: Scrape per-game data
# --------------------------
def get_bbr_per_game_stats(season_year):
    """
    Fetch per-game statistics for NBA players for the given season from Basketball Reference.
    Returns a pandas DataFrame with:
    Player, Team, Season, PTS_per_game, AST_per_game, FG_pct, TRB_per_game,
    BLK_per_game, STL_per_game, 3P_pct, TOV_per_game, PF_per_game
    """
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_year}_per_game.html"
    tables = pd.read_html(url)
    df = tables[0]
    #show(df)




    # Remove repeated headers and empty names
    df = df[df["Rk"] != "Rk"].copy()
    df = df.dropna(subset=["Player"])

    # Handle traded players (keep "TOT" if it exists)
    df = df.drop_duplicates(subset=["Player", "Team"], keep="first")
    if "Team" in df.columns:
        df = pd.concat(
            [df[df["Team"] != "TOT"], df[df["Team"] == "TOT"]],
            ignore_index=True
        )

    rename_map = {
        "Player": "Player",
        "Team": "Team",
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

    # Add season column (formatted like 2022-23)
    df2["Season"] = f"{season_year - 1}-{str(season_year)[-2:]}"

    # Convert to numeric where appropriate
    numeric_cols = [c for c in df2.columns if c.endswith("_per_game") or c.endswith("_pct")]
    df2[numeric_cols] = df2[numeric_cols].apply(pd.to_numeric, errors="coerce")

    df2.reset_index(drop=True, inplace=True)
    return df2


# --------------------------
# Main: Loop through multiple seasons and save
# --------------------------
if __name__ == "__main__":
    all_seasons = []

    for year in range(2000, 2026):
        try:
            season_df = get_bbr_per_game_stats(year)
            all_seasons.append(season_df)

            file_name = f"nba_per_game_stats_{year}.csv"
            season_df.to_csv(file_name, index=False)
            print(f"✅ Saved {file_name}")

            # polite delay to avoid blocking
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Error fetching season {year}: {e}")
            time.sleep(3)

    # Combine all into one dataset
    combined_df = pd.concat(all_seasons, ignore_index=True)
    combined_df.to_csv("nba_per_game_stats_all_2000_2025.csv", index=False)
    print("📁 Combined file saved: nba_per_game_stats_all_2000_2025.csv")

