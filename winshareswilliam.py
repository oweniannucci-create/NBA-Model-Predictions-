import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.library.parameters import Season
import time

# ==============================
# 1️⃣ Fetch Win Shares from Basketball Reference
# ==============================

def get_bbr_winshares(season_end_year=2025):
    """Scrape Win Shares from Basketball Reference advanced stats page."""
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}_advanced.html"
    tables = pd.read_html(url)
    df = tables[0]
    df = df[df['Rk'] != 'Rk']  # Remove duplicate headers
    df['WS'] = pd.to_numeric(df['WS'], errors='coerce')
    df = df[['Player', 'Tm', 'WS']]
    df.rename(columns={'Tm': 'TEAM_ABBREVIATION'}, inplace=True)
    return df

# ==============================
# 2️⃣ Fetch Per-Game Stats from NBA API
# ==============================

def get_nba_basic_stats(season="2024-25"):
    """Fetch basic per-game stats using nba_api."""
    data = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="PerGame"
    ).get_data_frames()[0]
    return data[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'PTS', 'REB', 'AST']]

# ==============================
# 3️⃣ Merge Both Sources
# ==============================

def merge_datasets(bbr_df, nba_df):
    """Merge Win Shares with NBA stats based on player name and team."""
    merged = pd.merge(
        nba_df,
        bbr_df,
        how='left',
        left_on=['PLAYER_NAME', 'TEAM_ABBREVIATION'],
        right_on=['Player', 'TEAM_ABBREVIATION']
    )
    merged.drop(columns=['Player'], inplace=True)
    return merged

# ==============================
# 4️⃣ Pivot to Team → Players columns
# ==============================

def pivot_team_player_stats(merged_df):
    """Pivot data so each team is one row, players’ stats as columns."""
    pivot = merged_df.pivot_table(
        index='TEAM_ABBREVIATION',
        columns='PLAYER_NAME',
        values=['PTS', 'REB', 'AST', 'WS'],
        fill_value=0
    )
    pivot.columns = [f"{stat}_{player}" for stat, player in pivot.columns]
    pivot.reset_index(inplace=True)
    return pivot

# ==============================
# 5️⃣ Run the Pipeline
# ==============================

if __name__ == "__main__":
    print("Fetching Win Shares from Basketball Reference...")
    ws_df = get_bbr_winshares(2025)
    time.sleep(1)

    print("Fetching per-game stats from nba_api...")
    nba_df = get_nba_basic_stats("2024-25")

    print("Merging datasets...")
    merged_df = merge_datasets(ws_df, nba_df)

    print("Pivoting team-player stats...")
    team_player_stats = pivot_team_player_stats(merged_df)

    # Save results
    merged_df.to_csv("nba_players_with_winshares.csv", index=False)
    team_player_stats.to_csv("nba_team_player_summary.csv", index=False)

    print("✅ Done! Files saved:")
    print("- nba_players_with_winshares.csv")
    print("- nba_team_player_summary.csv")


