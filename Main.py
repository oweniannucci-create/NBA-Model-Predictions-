import pandas as pd

# ---- Load CSV ----
games_df = pd.read_csv('Data/Games.csv', low_memory=False)

# ---- Columns in your CSV ----
HOME_TEAM_COL = "hometeamName"
AWAY_TEAM_COL = "awayteamName"
HOME_PTS_COL = "homeScore"
AWAY_PTS_COL = "awayScore"

# ---- Standardize team names ----
games_df[HOME_TEAM_COL] = games_df[HOME_TEAM_COL].str.strip()
games_df[AWAY_TEAM_COL] = games_df[AWAY_TEAM_COL].str.strip()

# ---- Current NBA teams mapping ----
# CSV names -> Standard abbreviations
team_mapping = {
    'Hawks': 'ATL', 'Celtics': 'BOS', 'Nets': 'BKN', 'Hornets': 'CHA', 'Bulls': 'CHI',
    'Cavaliers': 'CLE', 'Mavericks': 'DAL', 'Nuggets': 'DEN', 'Pistons': 'DET',
    'Warriors': 'GSW', 'Rockets': 'HOU', 'Pacers': 'IND', 'Clippers': 'LAC',
    'Lakers': 'LAL', 'Grizzlies': 'MEM', 'Heat': 'MIA', 'Bucks': 'MIL',
    'Timberwolves': 'MIN', 'Pelicans': 'NOP', 'Knicks': 'NYK', 'Thunder': 'OKC',
    'Magic': 'ORL', '76ers': 'PHI', 'Suns': 'PHX', 'Trail Blazers': 'POR',
    'Kings': 'SAC', 'Spurs': 'SAS', 'Raptors': 'TOR', 'Jazz': 'UTA',
    'Wizards': 'WAS'
}

# ---- Filter only games with current teams ----
games_df['Home_Abbr'] = games_df[HOME_TEAM_COL].map(team_mapping)
games_df['Away_Abbr'] = games_df[AWAY_TEAM_COL].map(team_mapping)
games_df = games_df.dropna(subset=['Home_Abbr','Away_Abbr'])

# ---- Determine winner/loser ----
games_df['Winner'] = games_df.apply(
    lambda x: x['Home_Abbr'] if x[HOME_PTS_COL] > x[AWAY_PTS_COL] else x['Away_Abbr'], axis=1
)
games_df['Loser'] = games_df.apply(
    lambda x: x['Away_Abbr'] if x[HOME_PTS_COL] > x[AWAY_PTS_COL] else x['Home_Abbr'], axis=1
)

# ---- Initialize win/loss records ----
current_teams = list(team_mapping.values())
records = {team: {opp: {"W":0, "L":0} for opp in current_teams if opp != team} for team in current_teams}

# ---- Count wins/losses ----
for _, row in games_df.iterrows():
    winner, loser = row['Winner'], row['Loser']
    records[winner][loser]['W'] += 1
    records[loser][winner]['L'] += 1

# ---- Build win percentage table ----
win_pct_matrix = pd.DataFrame(index=current_teams, columns=current_teams, dtype=float)

for team in current_teams:
    for opp in current_teams:
        if team == opp:
            win_pct_matrix.loc[team, opp] = None
        else:
            W = records[team][opp]['W']
            L = records[team][opp]['L']
            total = W + L
            win_pct_matrix.loc[team, opp] = round((W / total) * 100, 2) if total > 0 else None

# ---- Print win percentages ----
print("\n🏀 NBA Teams All-Time Win Percentages (%):\n")
print(win_pct_matrix.fillna("-"))

# ---- Save to CSV ----
win_pct_matrix.to_csv('NBA_Win_Percentages.csv')
print("\n✅ Saved as 'NBA_Win_Percentages.csv'")
