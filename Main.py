from sklearn.metrics import classification_report

import DataFetcher
import travel_distance
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import RidgeClassifier
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score




games_df = DataFetcher.get_cleaned_games_with_winner_column()
stats_df = DataFetcher.get_teamaveragestatistics_from_year()
draft_df = DataFetcher.get_average_draft_data()
rest_days = DataFetcher.get_rest_days()
player_stats = pd.read_csv("nba_per_game_stats_all_2000_2025.csv")
city_populations = DataFetcher.get_city_population()

player_winshare = pd.read_csv('nba_players_with_winshares_all_2000_2025.csv').sort_values(['Season', 'TEAM_ABBREVIATION', 'MP'], ascending=[True, True, True])

print(games_df.info())
print(stats_df.info())
print(draft_df.info())
print(player_stats.info())
print(rest_days.info())
print(city_populations.info())
print(player_winshare.info())


nba_team_abbreviations = {
    "ATL": "Hawks",
    "BOS": "Celtics",
    "BKN": "Nets",
    "BRK": "Nets",
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
    "MEM": "Grizzlies",
    "MIA": "Heat",
    "MIL": "Bucks",
    "MIN": "Timberwolves",
    "NOP": "Pelicans",
    "NOH": "Pelicans",
    "NYK": "Knicks",
    "OKC": "Thunder",
    "ORL": "Magic",
    "PHI": "76ers",
    "PHX": "Suns",
    "PHO": "Suns",
    "POR": "Trail Blazers",
    "SAC": "Kings",
    "SAS": "Spurs",
    "TOR": "Raptors",
    "UTA": "Jazz",
    "WAS": "Wizards",
    "NJN": "Nets",
    "SEA": "SuperSonics",
    "VAN": "Grizzlies"
}

def drop_columns_from_merged(merged_df):
    columns_to_drop = ['away_City', 'away_Year', 'home_City', 'home_Year', 'census_year', 'away_teamname', 'home_teamname', 'away_TEAM_ABBREVIATION',
                       'away_Season_y', 'away_Team_y', 'away_Team_x', 'away_Season_x',
                       'home_Season_y', 'home_Team_y', 'home_Team_x', 'home_Season_x', 'awayteamname', 'hometeamname', 'awayteamid',
                       'hometeamid', 'awayscore', 'homescore', 'prev_season', 'season', 'seriesgamenumber', 'gamesublabel', 'gamelabel', 'gametype', 'winner',
                       'home_TEAM_ABBREVIATION', 'home_gameDate', 'away_gameDate', 'hometeamcity', 'awayteamcity', 'gamedate', 'gameid']

    merged_df = merged_df.drop(columns_to_drop, axis=1)
    for i in range(1, 16):
        merged_df = merged_df.drop('home_Pos_p' + str(i), axis=1)
        merged_df = merged_df.drop('home_Player_p' + str(i), axis=1)
        merged_df = merged_df.drop('away_Pos_p' + str(i), axis=1)
        merged_df = merged_df.drop('away_Player_p' + str(i), axis=1)

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
    games = games[games['season_start'] >= 2000].copy()

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
    games['gamedate'] = pd.to_datetime(games['gamedate'])

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

merged = combine_game_team_draft_data(games_df, stats_df, draft_df, player_winshare, player_stats, city_populations)
merged = drop_columns_from_merged(merged)
merged = merged.fillna(0)


target = merged['winner_binary']
predict = merged.drop('winner_binary', axis=1)

x_train, x_test, y_train, y_test = train_test_split(predict, target, test_size=0.2, random_state=6)


scaler=StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.fit_transform(x_test)


for side in ["home", "away"]:
    for i in range(1, 16):
        col = f"{side}_Awards_p{i}"
        if col in merged.columns:
            merged.drop(columns=[col], inplace=True)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(x_train, y_train)

#Accuracy
y_pred = model.predict(x_test)
print("Accuracy：", accuracy_score(y_test, y_pred))
model.fit(x_train, y_train)
#Features searching
importances = pd.Series(model.feature_importances_, index=predict.columns)

#50 top feature
top_features = importances.sort_values(ascending=False).head(50)

print("Most important features:")
print(top_features)