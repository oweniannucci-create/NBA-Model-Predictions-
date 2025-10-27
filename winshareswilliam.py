import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.library.parameters import Season
import time
from pandasgui import show

# ==============================
# 1️⃣ Fetch Win Shares from Basketball Reference
# ==============================

def get_bbr_winshares(season_end_year=2025):
    """Scrape Win Shares from Basketball Reference advanced stats page."""
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}_advanced.html"
    tables = pd.read_html(url)
    df = tables[0]

    # Remove duplicate headers that appear throughout the table
    df = df[df["Rk"] != "Rk"]

    # Convert numeric columns
    df["WS"] = pd.to_numeric(df["WS"], errors="coerce")

    # Keep relevant columns
    #df = df[["Player", "Pos", "Age", "Team", "G", "MP", "PER", "WS"]]

    # Rename 'Tm' for clarity
    df.rename(columns={"Team": "TEAM_ABBREVIATION"}, inplace=True)

    # Add season column
    df["Season"] = f"{season_end_year - 1}-{str(season_end_year)[-2:]}"
    return df


if __name__ == "__main__":
    all_seasons = []

    for year in range(2000, 2026):
        print(f"Fetching Win Shares from Basketball Reference for {year} season...")

        # Fetch data
        ws_df = get_bbr_winshares(year)
        time.sleep(1)  # small delay to avoid rate limits if scraping

        # Save individual season file
        file_name = f"nba_players_with_winshares_{year}.csv"
        ws_df.to_csv(file_name, index=False)
        all_seasons.append(ws_df)

        print(f"✅ Done saving {file_name}")

    print("\n🎯 All seasons (2000–2025) have been processed and saved.")

    # Combine all data and save one master CSV
    all_data = pd.concat(all_seasons, ignore_index=True)
    all_data.to_csv("nba_players_with_winshares_all_2000_2025.csv", index=False)
    print("📁 Combined file saved: nba_players_with_winshares_all_2000_2025.csv")
