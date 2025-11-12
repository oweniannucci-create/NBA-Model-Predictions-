import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import DataFetcher

# ------------------- PART 1: Win Percentage Calculation -------------------

print("🏀 Loading Games.csv and calculating head-to-head win percentages...")

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
team_mapping = {
    'Hawks': 'ATL', 'Celtics': 'BOS', 'Nets': 'BKN', 'Hornets': 'CHA', 'Bulls': 'CHI',
    'Cavaliers': 'CLE', 'Mavericks': 'DAL', 'Nuggets': 'DEN', 'Pistons': 'DET',
    'Warriors': 'GSW', 'Rockets': 'HOU', 'Pacers': 'IND', 'Clippers': 'LAC',
    'Lakers': 'LAL', 'Grizzlies': 'MEM', 'Heat': 'MIA', 'Bucks': 'MIL',
    'Timberwolves': 'MIN', 'Pelicans': 'NOP', 'Knicks': 'NYK', 'Thunder': 'OKC',
    'Magic': 'ORL', '76ers': 'PHI', 'Suns': 'PHX', 'Trail Blazers': 'POR',
    'Kings': 'SAC', 'Spurs': 'SAS', 'Raptors': 'TOR', 'Jazz': 'UTA', 'Wizards': 'WAS', 'SuperSonics':'SEA', 'Bobcats':'CHA'
}

# ---- Map and filter only current teams ----
games_df['Home_Abbr'] = games_df[HOME_TEAM_COL].map(team_mapping)
games_df['Away_Abbr'] = games_df[AWAY_TEAM_COL].map(team_mapping)
games_df = games_df.dropna(subset=['Home_Abbr', 'Away_Abbr'])

# ---- Determine winners/losers ----
games_df['Winner'] = games_df.apply(
    lambda x: x['Home_Abbr'] if x[HOME_PTS_COL] > x[AWAY_PTS_COL] else x['Away_Abbr'], axis=1
)
games_df['Loser'] = games_df.apply(
    lambda x: x['Away_Abbr'] if x[HOME_PTS_COL] > x[AWAY_PTS_COL] else x['Home_Abbr'], axis=1
)

# ---- Initialize win/loss dictionary ----
current_teams = list(team_mapping.values())
records = {team: {opp: {"W": 0, "L": 0} for opp in current_teams if opp != team} for team in current_teams}

# ---- Count wins/losses ----
for _, row in games_df.iterrows():
    winner, loser = row['Winner'], row['Loser']

    # Skip self-matches (e.g., Hornets/Bobcats merged to same abbrev)
    if winner == loser:
        continue

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

# ---- Save to CSV ----
win_pct_matrix.to_csv('NBA_Win_Percentages.csv')
print("✅ Saved head-to-head win percentages as 'NBA_Win_Percentages.csv'")

# ------------------- PART 2: Model Data Preparation -------------------

print("\n📊 Fetching and combining datasets for modeling...")

games_df = DataFetcher.get_cleaned_games_with_winner_column()
stats_df = DataFetcher.get_teamaveragestatistics_from_year()
draft_df = DataFetcher.get_average_draft_data()

print(games_df.info())
print(stats_df.info())
print(draft_df.info())

def combine_game_team_draft_data(games_df, team_stats_df, draft_df):
    # --- Normalize columns ---
    games_df.columns = games_df.columns.str.lower()
    team_stats_df.columns = team_stats_df.columns.str.lower()
    draft_df.columns = draft_df.columns.str.lower()

    games_df['season'] = games_df['season'].astype(str)
    team_stats_df['season'] = team_stats_df['season'].astype(str)
    draft_df['season'] = draft_df['season'].astype(str)

    def previous_season(season_str):
        try:
            start, end = map(int, season_str.split('-'))
            return f"{start-1}-{end-1}"
        except:
            return None

    games_df['prev_season'] = games_df['season'].apply(previous_season)

    # --- Prep for merging ---
    home_stats = team_stats_df.add_prefix('home_')
    away_stats = team_stats_df.add_prefix('away_')
    home_draft = draft_df.add_prefix('home_')
    away_draft = draft_df.add_prefix('away_')

    home_stats = home_stats.rename(columns={'home_season': 'prev_season', 'home_teamname': 'hometeamname'})
    away_stats = away_stats.rename(columns={'away_season': 'prev_season', 'away_teamname': 'awayteamname'})
    home_draft = home_draft.rename(columns={'home_season': 'prev_season', 'home_team_name': 'hometeamname'})
    away_draft = away_draft.rename(columns={'away_season': 'prev_season', 'away_team_name': 'awayteamname'})

    merged = (
        games_df
        .merge(home_stats, on=['prev_season', 'hometeamname'], how='left')
        .merge(away_stats, on=['prev_season', 'awayteamname'], how='left')
        .merge(home_draft, on=['prev_season', 'hometeamname'], how='left')
        .merge(away_draft, on=['prev_season', 'awayteamname'], how='left')
    )

    columns_to_drop = ["gamedate", "arenaid", "hometeamcity", "awayteamcity", "seriesgamenumber",
                       "gamelabel", "gamesublabel", "attendance", "homescore", "awayscore",
                       "gameid", "gametype", "winner", "hometeamid", "awayteamid",
                       "hometeamname", "awayteamname", "season", "prev_season"]
    merged = merged.drop(columns=columns_to_drop, errors="ignore", axis=1)
    merged = merged.drop_duplicates(subset=['gameid'], errors="ignore").reset_index(drop=True)

    merged.to_csv("combined_games_team_draft.csv", index=False)
    print("✅ Combined dataset created: combined_games_team_draft.csv")
    print(f"Shape: {merged.shape}")

    return merged

combined_df = combine_game_team_draft_data(games_df, stats_df, draft_df)

# ------------------- PART 3: Neural Network Training -------------------

target = combined_df["winner_binary"]
predict = combined_df.drop("winner_binary", axis=1)

x_train, x_test, y_train, y_test = train_test_split(predict, target, test_size=0.2, random_state=6)

tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir="C:/Users/steve/PycharmProjects/machine-learning/logs",
    histogram_freq=1,
    embeddings_freq=1,
    update_freq="epoch",
)

nn_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(42,)),
    tf.keras.layers.Dense(84, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

nn_model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
                 loss='binary_crossentropy',
                 metrics=['accuracy'])

history = nn_model.fit(
    x_train, y_train, epochs=100, batch_size=32,
    validation_split=0.2, callbacks=[tensorboard_callback]
)

y_pred = (nn_model.predict(x_test) > 0.5).astype(int)
print(classification_report(y_test, y_pred))

print("\n✅ Model training complete!")
