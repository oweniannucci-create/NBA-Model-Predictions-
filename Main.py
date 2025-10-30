from sklearn.metrics import classification_report

import DataFetcher
import travel_distance
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# import tensorflow as tf
import pandas as pd
from pandasgui import show




games_df = DataFetcher.get_cleaned_games_with_winner_column()
stats_df = DataFetcher.get_teamaveragestatistics_from_year()
draft_df = DataFetcher.get_average_draft_data()
rest_days = DataFetcher.get_rest_days()
player_stats = pd.read_csv("nba_per_game_stats_all_2000_2025.csv")
city_populations = DataFetcher.get_city_population()
show(city_populations)
player_winshare = pd.read_csv('nba_players_with_winshares_all_2000_2025.csv').sort_values(['Season', 'TEAM_ABBREVIATION', 'MP'], ascending=[True, True, True])

print(games_df.info())
print(stats_df.info())
print(draft_df.info())
print(player_stats.info())
print(rest_days.info())
print(city_populations.info())
print(player_winshare.info())
stats = [
        "teamScore",
        "assists",
        "reboundsDefensive",
        "reboundsOffensive",
        "reboundsTotal",
        "steals",
        "blocks",
        "turnovers",
        "foulsPersonal",
        "fieldGoalsMade",
        "fieldGoalsAttempted",
        "fieldGoalsPercentage",
        "threePointersMade",
        "threePointersAttempted",
        "threePointersPercentage",
        "freeThrowsMade",
        "freeThrowsAttempted",
        "freeThrowsPercentage",
        "plusMinusPoints",
        "number_of_picks",
        "average_overall_pick"
    ]


def get_season_records():
    team_results = []

    # show(games_df)
    for _, row in games_df.iterrows():
        winner = row['winner']
        home = row['hometeamid']
        away = row['awayteamid']
        season = row['season']
        home_team = row['hometeamname']
        away_team = row['awayteamname']

        # Home result
        team_results.append({

            'teamname': home_team,
            'season': season,
            'win': 1 if winner == home else 0,
            'loss': 0 if winner == home else 1
        })

        # Away result
        team_results.append({
            'teamname': away_team,
            'season': season,
            'win': 1 if winner == away else 0,
            'loss': 0 if winner == away else 1
        })

    record_df = pd.DataFrame(team_results)

    # Aggregate wins/losses
    record_df = record_df.groupby(['teamname', 'season']).sum().reset_index()
    record_df['win_pct'] = record_df['win'] / (record_df['win'] + record_df['loss'])

    return record_df
def combine_game_team_draft_data(games_df, team_stats_df, draft_df):
    # --- 1️⃣ Normalize and prep columns ---
    games_df.columns = games_df.columns.str.lower()
    team_stats_df.columns = team_stats_df.columns.str.lower()
    draft_df.columns = draft_df.columns.str.lower()

    games_df['season'] = games_df['season'].astype(str)
    team_stats_df['season'] = team_stats_df['season'].astype(str)
    draft_df['season'] = draft_df['season'].astype(str)

    draft_df["number_of_picks"] = draft_df["number_of_picks"].fillna(0)
    draft_df["average_overall_pick"] = draft_df["average_overall_pick"].fillna(-1)

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
    merged["travel_distance_km"] = merged.apply(
        lambda row: travel_distance.get_distance_between_cities(row["hometeamcity"], row["awayteamcity"]),
        axis=1
    )
    show(merged)
    #home_team_dummies = pd.get_dummies(merged['hometeamname'], prefix='home_team')
    #away_team_dummies = pd.get_dummies(merged['awayteamname'], prefix='away_team')
    #merged = pd.concat([merged, home_team_dummies, away_team_dummies], axis=1)

    # --- 4️⃣ Cleanup ---
    merged = merged.drop_duplicates(subset=['gameid']).reset_index(drop=True)
    merged["season_start"] = merged["season"].str.split("-").str[0].astype(int)
    merged = merged[merged["season_start"] >= 2000].copy()
    columns_to_drop = ["gamedate","arenaid", "hometeamcity", "awayteamcity", "seriesgamenumber", "gamelabel", "gamesublabel",
                       "attendance", "homescore", "awayscore", "gameid", "gametype","winner","hometeamid", "awayteamid", "prev_season", 'season_start']

    merged = merged.drop(columns=columns_to_drop, errors="ignore", axis=1)
    print(merged.info())
    merged.to_csv("combined_games_team_draft.csv", index=False)
    print("✅ Combined dataset created successfully: combined_games_team_draft.csv")
    print(f"Shape: {merged.shape}")

    return merged

combined_df = combine_game_team_draft_data(games_df, stats_df, draft_df)

#show(combined_df)
# for col in [s.lower() for s in stats]:
#     combined_df[f'diff_{col}'] = combined_df[f'home_{col}'] - combined_df[f'away_{col}']
#
# a_vs_b = combined_df.copy()
# a_vs_b["team_A"] = a_vs_b["hometeamname"]
# a_vs_b["team_B"] = a_vs_b["awayteamname"]
# a_vs_b["label"] = a_vs_b["winner_binary"]
#
# b_vs_a = combined_df.copy()
# b_vs_a["team_A"] = b_vs_a["awayteamname"]
# b_vs_a["team_B"] = b_vs_a["hometeamname"]
# b_vs_a["label"] = 1 - b_vs_a["winner_binary"]
# b_vs_a[[c for c in a_vs_b.columns if c.startswith("diff_")]]=b_vs_a[[c for c in a_vs_b.columns if c.startswith("diff_")]].apply(lambda x: -x)
#
# a_vs_b = a_vs_b[["team_A", "team_B", "label"] + [c for c in a_vs_b.columns if c.startswith("diff_")]]
# b_vs_a = b_vs_a[["team_A", "team_B", "label"] + [c for c in b_vs_a.columns if c.startswith("diff_")]]
#
# combined = pd.concat([a_vs_b, b_vs_a], ignore_index=True)
# combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)

#show(combined)

# combined = pd.get_dummies(combined, columns=["team_A", "team_B"], drop_first=False)

#show(combined)

#combined_df = combined_df.drop(columns=['home_'+s.lower() for s in stats], errors="ignore", axis=1)
#combined_df = combined_df.drop(columns=['away_'+s.lower() for s in stats], errors="ignore", axis=1)

#show(combined_df)

# target = combined['label']
# predict = combined.drop('label', axis=1)
#
# x_train, x_test, y_train, y_test = train_test_split(predict, target, test_size=0.2, random_state=6)

# x_train = combined_df[combined_df['season'] != '2024-2025']
# x_test = combined_df[combined_df['season'] == '2024-2025']
#
# x_train = x_train.drop('season', axis=1)
# x_test = x_test.drop('season', axis=1)
#
# y_train = x_train["winner_binary"]
# x_train = x_train.drop("winner_binary",axis=1)
#
# y_test = x_test['winner_binary']
# x_test = x_test.drop('winner_binary', axis=1)

# scaler=StandardScaler()
# x_train = scaler.fit_transform(x_train)
# x_test = scaler.fit_transform(x_test)
#
#
# tensorboard_callback = tf.keras.callbacks.TensorBoard(
#     log_dir="C:/Users/steve/PycharmProjects/machine-learning/logs",
#     histogram_freq=1,  # How often to log histogram visualizations
#     embeddings_freq=1,  # How often to log embedding visualizations
#     update_freq="epoch",
# )
#
# nn_model = tf.keras.Sequential([
#     tf.keras.layers.Input(shape=(85,)),
#     tf.keras.layers.Dense(202, activation='relu'),
#     tf.keras.layers.Dense(54, activation='relu'),
#     tf.keras.layers.Dense(12, activation='relu'),
#     tf.keras.layers.Dense(80, activation='relu'),
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
# print(y_pred)