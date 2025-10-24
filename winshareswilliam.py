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
    show(df)
    #df = df[df['Rk'] != 'Rk']  # Remove duplicate headers
    #df['WS'] = pd.to_numeric(df['WS'], errors='coerce')
    #df = df[['Player', 'Team', 'WS']]
    df.rename(columns={'Team': 'TEAM_ABBREVIATION'}, inplace=True)
    return df


if __name__ == "__main__":
    for year in range(2000, 2026):
        print(f"Fetching Win Shares from Basketball Reference for {year} season...")

        # Fetch data
        ws_df = get_bbr_winshares(year)
        time.sleep(1)  # small delay to avoid rate limits if scraping

        # Save individual season file
        file_name = f"nba_players_with_winshares_{year}.csv"
        ws_df.to_csv(file_name, index=False)

        print(f"✅ Done saving {file_name}")

    print("\n🎯 All seasons (2000–2025) have been processed and saved.")

    # Combine all individual season files into one big CSV
    all_data = pd.concat(
        [pd.read_csv(f"nba_players_with_winshares_{year}.csv") for year in range(2000, 2026)],
        ignore_index=True
    )

    all_data.to_csv("nba_players_with_winshares_all_2000_2025.csv", index=False)
    print("📁 Combined file saved: nba_players_with_winshares_all_2000_2025.csv")



