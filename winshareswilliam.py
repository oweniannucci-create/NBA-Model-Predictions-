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
    print("Fetching Win Shares from Basketball Reference...")
    ws_df = get_bbr_winshares()
    time.sleep(1)


    # Save results
    ws_df.to_csv("nba_players_with_winshares.csv", index=False)

    print("✅ Done! Files saved:")
    print("- nba_players_with_winshares.csv")
    print("- nba_team_player_summary.csv")


