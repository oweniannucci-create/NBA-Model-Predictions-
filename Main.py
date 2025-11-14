from sklearn.metrics import classification_report

import DataFetcher
import travel_distance
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import pandas as pd
import re
from pandasgui import show

nba_team_abbreviations_full = {
    "ATL": "Atlanta Hawks",
    "BOS": "Boston Celtics",
    "BKN": "Brooklyn Nets",
    "BRK": "Brooklyn Nets",
    "CHH": "Charlotte Hornets",
    "CHA": "Charlotte Hornets",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DAL": "Dallas Mavericks",
    "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons",
    "GSW": "Golden State Warriors",
    "HOU": "Houston Rockets",
    "IND": "Indiana Pacers",
    "LAC": "LA Clippers",
    "LAL": "LA Lakers",
    "MEM": "Memphis Grizzlies",
    "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks",
    "MIN": "Minnesota Timberwolves",
    "NOP": "New Orleans Pelicans",
    "NOH": "New Orleans Pelicans",
    "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder",
    "ORL": "Orlando Magic",
    "PHI": "Philadelphia 76ers",
    "PHX": "Phoenix Suns",
    "PHO": "Phoenix Suns",
    "POR": "Portland Trail Blazers",
    "SAC": "Sacramento Kings",
    "SAS": "San Antonio Spurs",
    "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz",
    "WAS": "Washington Wizards",
    "NJN": "Brooklyn Nets",
    "SEA": "Seattle SuperSonics",
    "VAN": "Memphis Grizzlies"
}
nba_team_abbreviations = {
    "ATL": "Hawks",
    "BOS": "Celtics",
    "NJN": "Nets",
    "BRK": "Nets",
    "BKN": "Nets",
    "CHH": "Hornets",
    "CHA": "Hornets",
    "CHI": "Bulls",
    "CLE": "Cavaliers",
    "DAL": "Mavericks",
    "DEN": "Nuggets",
    "DET": "Pistons",
    "GSW": "Warriors",
    "HOU": "Rockets",
    "IND": "Pacers",
    "LAC": "Clippers",
    "LAL": "Lakers",
    "VAN": "Grizzlies",
    "MEM": "Grizzlies",
    "MIA": "Heat",
    "MIL": "Bucks",
    "MIN": "Timberwolves",
    "NOH": "Pelicans",
    "NOP": "Pelicans",
    "NYK": "Knicks",
    "OKC": "Thunder",
    "ORL": "Magic",
    "PHI": "76ers",
    "PHO": "Suns",
    "PHX": "Suns",
    "POR": "Trail Blazers",
    "SAC": "Kings",
    "SAS": "Spurs",
    "TOR": "Raptors",
    "UTA": "Jazz",
    "WAS": "Wizards",
    "SEA": "SuperSonics"
}

# name_to_abbrev = {v: k for k, v in nba_team_abbreviations.items()}
# name_to_abbrev['Bobcats']="CHA"
#
#
# valid_teams = set(name_to_abbrev.keys())
# games_df = DataFetcher.get_cleaned_games_with_winner_column()
# stats_df = DataFetcher.get_teamaveragestatistics_from_year()
# draft_df = DataFetcher.get_average_draft_data()
# rest_days = DataFetcher.get_rest_days()
# player_stats = pd.read_csv("nba_per_game_stats_all_2000_2025.csv")
# city_populations = DataFetcher.get_city_population()
# player_winshare = pd.read_csv('nba_players_with_winshares_all_2000_2025.csv').sort_values(['Season', 'TEAM_ABBREVIATION', 'MP'], ascending=[True, True, True])
# win_matrix = pd.read_csv('NBA_Win_Percentages.csv', index_col=0)
#
#
#
# print(games_df.info())
# print(stats_df.info())
# print(draft_df.info())
# print(player_stats.info())
# print(rest_days.info())
# print(city_populations.info())
# print(player_winshare.info())
#
#
# # -----------------------------
# # Map abbreviations to full team names (with city) to match trade CSV
# # -----------------------------
#
#
# # Add full team name column to player_stats
# player_stats['TEAM_FULL_NAME'] = player_stats['Team'].map(nba_team_abbreviations_full)
# player_winshare['TEAM_FULL_NAME'] = player_winshare['TEAM_ABBREVIATION'].map(nba_team_abbreviations_full)
#
# # --- Check mapping worked ---
# # print(player_stats[['Player', 'Team', 'TEAM_FULL_NAME']].head(10))
#
# # -----------------------------
# # Load trade data and adjust stats for traded players
# # -----------------------------
# trades = pd.read_csv("nba_trades_combined_sorted.csv")  # Columns: Player, From_Team, To_Team, Year
#
# # # Read the trade CSV into a variable
# # trade_data = pd.read_csv("nba_trades_combined_sorted.csv")
# #
# # # Check a specific player
# # print(trade_data[trade_data['Player'] == 'Kevin Durant'])
#
#
#
# # Map abbreviations in trade data to full team names (using existing mapping)
# if 'From' in trades.columns and 'To' in trades.columns:
#     trades['From'] = trades['From'].map(nba_team_abbreviations_full).fillna(trades['From'])
#     trades['To'] = trades['To'].map(nba_team_abbreviations_full).fillna(trades['To'])
#
# # Create a season mapping dictionary for all years 2003–2026
# season_mapping = {year: f"{year-1}-{str(year)[-2:]}" for year in range(2003, 2026)}
#
# # Apply this mapping to your trade data
# if 'Season' in trades.columns:
#     trades['Season'] = trades['Season'].map(season_mapping)



def update_player_stats_for_trades(player_stats, trades):
    """
    Reassign all stats in seasons where a player was traded to the new team (full team name).
    """
    def assign_team_by_trade(row):
        player = row['Player']
        season = row['Season']
        trade_info = trades[(trades['Player'] == player) & (trades['Season'] == season)]
        if not trade_info.empty:
            return trade_info.iloc[0]['To']  # Full team name from trades CSV
        return row['TEAM_FULL_NAME']  # Original mapped full name

    player_stats['TEAM_FULL_NAME'] = player_stats.apply(assign_team_by_trade, axis=1)
    return player_stats

# Apply trade adjustment

# player_stats = update_player_stats_for_trades(player_stats, trades)
# player_winshare = update_player_stats_for_trades(player_winshare, trades)
# inv_team_dict = {v: k for k, v in nba_team_abbreviations_full.items()}
# player_stats['Team']=player_stats['TEAM_FULL_NAME'].map(inv_team_dict)
# player_winshare['TEAM_ABBREVIATION']=player_winshare['TEAM_FULL_NAME'].map(inv_team_dict)
# player_winshare.drop('TEAM_FULL_NAME', axis=1)
# player_stats.drop('TEAM_FULL_NAME', axis=1)








#Comment


def get_win_pct(row):
    # Convert full names to abbreviations
    home_abbrev = name_to_abbrev.get(row["hometeamname"])
    away_abbrev = name_to_abbrev.get(row["awayteamname"])

    # Handle missing teams gracefully
    if home_abbrev not in win_matrix.index or away_abbrev not in win_matrix.columns:
        print(row["hometeamname"] +" or "+ row["awayteamname"] +" not in dictionary")
        return None

    return win_matrix.loc[home_abbrev, away_abbrev]

def drop_columns_from_merged(merged_df):
    columns_to_drop = ['away_City', 'away_Year', 'home_City', 'home_Year', 'census_year', 'away_teamname', 'home_teamname', 'away_TEAM_ABBREVIATION',
                       'away_Season_y', 'away_Team_y', 'away_Team_x', 'away_Season_x',
                       'home_Season_y', 'home_Team_y', 'home_Team_x', 'home_Season_x', 'awayteamname', 'hometeamname', 'awayteamid',
                       'hometeamid', 'awayscore', 'homescore', 'prev_season', 'season', 'seriesgamenumber', 'gamesublabel', 'gamelabel', 'gametype', 'winner',
                       'home_TEAM_ABBREVIATION', 'home_gameDate', 'away_gameDate', 'hometeamcity', 'awayteamcity', 'gamedate', 'gameid','season_end', 'status_text', 'played']

    merged_df = merged_df.drop(columns_to_drop, axis=1)
    for i in range(1, 16):
        merged_df = merged_df.drop('home_Pos_p' + str(i), axis=1)
        merged_df = merged_df.drop('home_Player_p' + str(i), axis=1)
        merged_df = merged_df.drop('away_Pos_p' + str(i), axis=1)
        merged_df = merged_df.drop('away_Player_p' + str(i), axis=1)
        merged_df = merged_df.drop('away_TEAM_FULL_NAME_adv_p' + str(i), axis=1)
        merged_df = merged_df.drop('home_TEAM_FULL_NAME_adv_p' + str(i), axis=1)
        merged_df = merged_df.drop('away_TEAM_FULL_NAME_stats_p' + str(i), axis=1)
        merged_df = merged_df.drop('home_TEAM_FULL_NAME_stats_p' + str(i), axis=1)

    for side in ["home", "away"]:
        for i in range(1, 16):
            col = f"{side}_Awards_p{i}"
            if col in merged_df.columns:
                merged_df.drop(columns=[col], inplace=True)
    return merged_df
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


def parse_awards(award_str):
    """Convert award string into dict of award -> numeric value"""
    if not isinstance(award_str, str) or award_str.strip() == "":
        return {}

    awards = {}
    for item in award_str.split(","):
        item = item.strip()
        if not item:
            continue
        # Match patterns like MVP-2, NBA1, AS, DEF2
        match = re.match(r"([A-Z]+)(?:-?(\d+))?", item)
        if match:
            key = match.group(1)
            val = match.group(2)
            awards[key] = int(val) if val else 1
    return awards


def expand_player_awards(df, side="home", num_players=15):
    """
    Expand award columns for all players for one team side (home/away)
    df: pandas DataFrame containing award columns
    side: "home" or "away"
    num_players: number of player slots
    """
    for i in range(1, num_players + 1):
        col = f"{side}_Awards_p{i}"
        if col in df.columns:
            expanded = df[col].apply(parse_awards).apply(pd.Series)
            expanded = expanded.add_prefix(f"{col}_")
            df = pd.concat([df, expanded], axis=1)
    return df


def combine_game_team_draft_data(games, team_stats, draft_data, player_advanced, player_stats, city_pop):
    # Define previous season label helper
    def previous_season(season_str):
        try:
            start, end = map(int, season_str.split('-'))
            return f"{start-1}-{end-1}"
        except:
            return None


    # Convert the season start year to integer
    games['season_start'] = games['season'].str.split('-').str[0].astype(int)

    # Keep only seasons starting in 2000 or later
    games = games[games['season_start'] >= 2005].copy()
    games["HomeWinPctVsAway"] = games.apply(get_win_pct, axis=1)

    # Optionally, drop the helper column
    games.drop(columns=['season_start'], inplace=True)

    # standardize column names for joining
    player_stats = player_stats.rename(columns={'Team': 'TEAM_ABBREVIATION', 'Season': 'Season'})
    player_advanced = player_advanced.rename(columns={'TEAM_ABBREVIATION': 'TEAM_ABBREVIATION', 'Season': 'Season'})

    # merge both player-level datasets
    player_full = pd.merge(
        player_advanced,
        player_stats,
        on=['Player', 'TEAM_ABBREVIATION', 'Season'],
        how='left',
        suffixes=('_adv', '_stats')
    )


    games['prev_season'] = games['season'].apply(previous_season)

    # rename to match naming scheme
    team_stats = team_stats.rename(columns={'teamName': 'Team', 'season': 'Season'})
    draft_data = draft_data.rename(columns={'TEAM_NAME': 'Team', 'SEASON': 'Season'})

    # # merge home and away versions
    # games = games.merge(
    #     team_stats.add_prefix('home_'),
    #     left_on=['hometeamname', 'prev_season'],
    #     right_on=['home_Team', 'home_Season'],
    #     how='left'
    # ).merge(
    #     team_stats.add_prefix('away_'),
    #     left_on=['awayteamname', 'prev_season'],
    #     right_on=['away_Team', 'away_Season'],
    #     how='left'
    # )

    # same idea for draft_data
    games = games.merge(
        draft_data.add_prefix('home_'),
        left_on=['hometeamname', 'prev_season'],
        right_on=['home_Team', 'home_Season'],
        how='left'
    ).merge(
        draft_data.add_prefix('away_'),
        left_on=['awayteamname', 'prev_season'],
        right_on=['away_Team', 'away_Season'],
        how='left'
    )

    #Merge rest days
    rest_days['gameDate'] = pd.to_datetime(rest_days['gameDate'])
    games['gamedate'] = pd.to_datetime(games['gamedate'], format='ISO8601')

    games = games.merge(
        rest_days.add_prefix('home_'),
        left_on=['hometeamname', 'gamedate'],
        right_on=['home_Team', 'home_gameDate'],
        how='left'
    ).merge(
        rest_days.add_prefix('away_'),
        left_on=['awayteamname', 'gamedate'],
        right_on=['away_Team', 'away_gameDate'],
        how='left'
    )

    #Top 15 players
    top_players = (
        player_full
        .sort_values(['Season', 'TEAM_ABBREVIATION', 'MP'], ascending=[True, True, False])
        .groupby(['Season', 'TEAM_ABBREVIATION'])
        .head(15)
        .copy()
    )

    # rank players 1–15 by minutes
    top_players['player_rank'] = top_players.groupby(['Season', 'TEAM_ABBREVIATION']).cumcount() + 1

    wide_players = top_players.pivot(
        index=['Season', 'TEAM_ABBREVIATION'],
        columns='player_rank'
    )

    # flatten MultiIndex columns
    wide_players.columns = [f"{stat}_p{rank}" for stat, rank in wide_players.columns]
    wide_players = wide_players.reset_index()
    wide_players['teamname'] = wide_players['TEAM_ABBREVIATION'].map(nba_team_abbreviations)
    wide_players['Season'] = wide_players['Season'].apply(lambda x: x.split('-')[0]+'-'+'20'+x.split('-')[1])
    #show(wide_players)

    games = games.merge(
        wide_players.add_prefix('home_'),
        left_on=['hometeamname', 'prev_season'],
        right_on=['home_teamname', 'home_Season'],
        how='left'
    ).merge(
        wide_players.add_prefix('away_'),
        left_on=['awayteamname', 'prev_season'],
        right_on=['away_teamname', 'away_Season'],
        how='left'
    )
    # Melt population df: index=year, columns=cities
    pop_long = city_pop.reset_index().melt(id_vars='index', var_name='City', value_name='Population')
    pop_long = pop_long.rename(columns={'index': 'Year'})

    # Map each season to census year
    def season_to_census(season):
        start = int(season.split('-')[0])
        if start < 2010:
            return 2000
        elif start < 2020:
            return 2010
        else:
            return 2020

    games['census_year'] = games['season'].apply(season_to_census)

    # Merge population data
    games = games.merge(
        pop_long.add_prefix('home_'),
        left_on=['hometeamcity', 'census_year'],
        right_on=['home_City', 'home_Year'],
        how='left'
    ).merge(
        pop_long.add_prefix('away_'),
        left_on=['awayteamcity', 'census_year'],
        right_on=['away_City', 'away_Year'],
        how='left'
    )

    games = expand_player_awards(games, side="home", num_players=15)
    games = expand_player_awards(games, side="away", num_players=15)

    return games


# merged = combine_game_team_draft_data(games_df, stats_df, draft_df, player_winshare, player_stats, city_populations)
# merged['away_travel_distance'] = merged.apply(lambda x: travel_distance.get_distance_between_cities(x['awayteamcity'], x['hometeamcity']), axis=1)
# #merged = drop_columns_from_merged(merged)
# merged = merged.fillna(0)
merged = pd.read_csv('total_training_set.csv')
merged.to_csv('total_training_set.csv', index=False)


merged["season_end"] = merged['season'].apply(lambda x: int(x.split("-")[1]))
# merged = merged[merged["gametype"] != "Playoffs"]
# merged = merged[merged["gametype"] != "Play-in Tournament"]

train = merged[merged['season_end'] < 2025 ]
test = merged[merged['season_end'] == 2025]

games_2024_25 = test[["hometeamname","awayteamname","gamedate","winner_binary"]]

train = drop_columns_from_merged(train)
test = drop_columns_from_merged(test)

y_train = train["winner_binary"]
x_train = train.drop(columns=["winner_binary"], axis=1)

y_test = test["winner_binary"]
x_test = test.drop(columns=["winner_binary"], axis=1)


# target = merged['winner_binary']
# predict = merged.drop('winner_binary', axis=1)
#
# x_train, x_test, y_train, y_test = train_test_split(predict, target, test_size=0.2, random_state=6)


scaler=StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Convert to DMatrix (XGBoost native format)
dtrain = xgb.DMatrix(x_train, label=y_train)
dtest = xgb.DMatrix(x_test, label=y_test)

params = {
    'objective': 'binary:logistic',
    'learning_rate': 0.01,
    'max_depth': 8,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'eval_metric': 'logloss',
    'seed': 42
}

# Evaluation sets
evals = [(dtrain, 'train'), (dtest, 'eval')]

# Train with early stopping
bst = xgb.train(
    params=params,
    dtrain=dtrain,
    num_boost_round=300,
    evals=evals,
    early_stopping_rounds=20,
    verbose_eval=True
)

y_prob_xgb = bst.predict(dtest)
# Make predictions
y_pred_xgb = (y_prob_xgb > 0.5).astype(int)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred_xgb)
print("Test Accuracy:", accuracy)
#rr = RidgeClassifier(alpha=1)

tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir="C:/Users/steve/PycharmProjects/machine-learning/logs",
    histogram_freq=1,  # How often to log histogram visualizations
    embeddings_freq=1,  # How often to log embedding visualizations
    update_freq="epoch",
)

early_stop = tf.keras.callbacks.EarlyStopping(
    patience=20, restore_best_weights=True, monitor='val_loss'
)

nn_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(1192,)),
    tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(1e-4)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(1e-4)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# sfs = SequentialFeatureSelector(rr, n_features_to_select=100, direction='forward', cv=KFold(n_splits=3, shuffle=True, random_state=42), scoring='accuracy', n_jobs=-1)
# sfs.fit(x_train, y_train)
# predictors = sfs.transform(x_train)
# print(predictors.info())
# print(predictors)
#
# rr.fit(x_train[predictors], y_train)

nn_model.compile(optimizer=tf.keras.optimizers.Adam(1e-4), loss='binary_crossentropy', metrics=['accuracy'])

history = nn_model.fit(x_train, y_train, epochs=20, batch_size=32, validation_split=0.2, callbacks=[tensorboard_callback, early_stop])

y_prob = nn_model.predict(x_test)

#Convert to 0s and 1s
y_pred = (y_prob > 0.5).astype(int)

games_2024_25["home_team_win_pred_nn"] = y_pred
games_2024_25["probability_home_team_win_nn"] = y_prob
games_2024_25["home_team_win_pred_xgb"] = y_pred_xgb
games_2024_25["probability_home_team_win_xgb"] = y_prob_xgb

print("Neural Network Report:")
print(classification_report(y_test,y_pred))

print("XGBoost Report:")
print(classification_report(y_test,y_pred_xgb))
show(games_2024_25)