#from sklearn.metrics import classification_report

import DataFetcher
#from sklearn.model_selection import train_test_split
#import tensorflow as tf
from pandasgui import show
import RestDate

games_df = DataFetcher.get_cleaned_games_with_winner_column()
stats_df = DataFetcher.get_teamaveragestatistics_from_year()
draft_df = DataFetcher.get_average_draft_data()
rest_days_df = RestDate.get_team_rest_days()

print(games_df.info())
print(stats_df.info())
print(draft_df.info())

def combine_game_team_draft_data(games_df, team_stats_df, draft_df):
    # --- 1️⃣ Normalize and prep columns ---
    games_df.columns = games_df.columns.str.lower()
    team_stats_df.columns = team_stats_df.columns.str.lower()
    draft_df.columns = draft_df.columns.str.lower()

    games_df['season'] = games_df['season'].astype(str)
    team_stats_df['season'] = team_stats_df['season'].astype(str)
    draft_df['season'] = draft_df['season'].astype(str)

    # Define previous season label helper
    def previous_season(season_str):
        try:
            start, end = map(int, season_str.split('-'))
            return f"{start-1}-{end-1}"
        except:
            return None

    games_df['prev_season'] = games_df['season'].apply(previous_season)

    # --- 2️⃣ Prepare copies of stats and draft data with unique column names ---
    home_stats = team_stats_df.add_prefix('home_')
    away_stats = team_stats_df.add_prefix('away_')

    home_draft = draft_df.add_prefix('home_')
    away_draft = draft_df.add_prefix('away_')

    # Rename join keys in each to match merge fields
    home_stats = home_stats.rename(columns={'home_season': 'prev_season', 'home_teamname': 'hometeamname'})
    away_stats = away_stats.rename(columns={'away_season': 'prev_season', 'away_teamname': 'awayteamname'})

    home_draft = home_draft.rename(columns={'home_season': 'prev_season', 'home_team_name': 'hometeamname'})
    away_draft = away_draft.rename(columns={'away_season': 'prev_season', 'away_team_name': 'awayteamname'})
  
    # --- 3️⃣ Merge sequentially without suffixes (no collisions possible) ---
    merged = (
        games_df
        .merge(home_stats, on=['prev_season', 'hometeamname'], how='left')
        .merge(away_stats, on=['prev_season', 'awayteamname'], how='left')
        .merge(home_draft, on=['prev_season', 'hometeamname'], how='left')
        .merge(away_draft, on=['prev_season', 'awayteamname'], how='left')
    )

    show(merged)
    # --- 4️⃣ Cleanup ---
    merged = merged.drop_duplicates(subset=['gameid']).reset_index(drop=True)
    columns_to_drop = ["gamedate","arenaid", "hometeamcity", "awayteamcity", "seriesgamenumber", "gamelabel", "gamesublabel",
                       "attendance", "homescore", "awayscore", "gameid", "gametype","winner","hometeamid", "awayteamid","hometeamname", "awayteamname", 'season', 'prev_season']
    merged = merged.drop(columns=columns_to_drop, errors="ignore", axis=1)
    
    merged.to_csv("combined_games_team_draft.csv", index=False)
    print("✅ Combined dataset created successfully: combined_games_team_draft.csv")
    print(f"Shape: {merged.shape}")

    return merged

combined_df = combine_game_team_draft_data(games_df, stats_df, draft_df)

#
# target = combined_df["winner_binary"]
# predict = combined_df.drop("winner_binary",axis=1)
#
# x_train, x_test, y_train, y_test = train_test_split(predict, target, test_size=0.2, random_state=6)
#
# tensorboard_callback = tf.keras.callbacks.TensorBoard(
#     log_dir="C:/Users/steve/PycharmProjects/machine-learning/logs",
#     histogram_freq=1,  # How often to log histogram visualizations
#     embeddings_freq=1,  # How often to log embedding visualizations
#     update_freq="epoch",
# )
#
# nn_model = tf.keras.Sequential([
#     tf.keras.layers.Input(shape=(42,)),
#     tf.keras.layers.Dense(84, activation='relu'),
#     tf.keras.layers.Dense(1, activation='sigmoid')
# ])
#
#
#
# nn_model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss='binary_crossentropy', metrics=['accuracy'])
#
# history = nn_model.fit(x_train, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[tensorboard_callback])
#
# y_pred = (nn_model.predict(x_test)>0.5).astype(int)
#
# print(classification_report(y_test,y_pred))