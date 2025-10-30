from nba_api.stats.endpoints import DraftHistory
import pandas as pd
import time
#from pandasgui import show


def get_city_population():
    # NBA team–city mapping
    nba_cities = {
        'Atlanta Hawks': 'Atlanta',
        'Boston Celtics': 'Boston',
        'Brooklyn Nets': 'Brooklyn',
        'Charlotte Hornets': 'Charlotte',
        'Chicago Bulls': 'Chicago',
        'Cleveland Cavaliers': 'Cleveland',
        'Dallas Mavericks': 'Dallas',
        'Denver Nuggets': 'Denver',
        'Detroit Pistons': 'Detroit',
        'Golden State Warriors': 'San Francisco',
        'Houston Rockets': 'Houston',
        'Indiana Pacers': 'Indianapolis',
        'Los Angeles Clippers': 'Los Angeles',
        'Los Angeles Lakers': 'Los Angeles',
        'Memphis Grizzlies': 'Memphis',
        'Miami Heat': 'Miami',
        'Milwaukee Bucks': 'Milwaukee',
        'Minnesota Timberwolves': 'Minneapolis',
        'New Orleans Pelicans': 'New Orleans',
        'New York Knicks': 'New York',
        'Oklahoma City Thunder': 'Oklahoma City',
        'Orlando Magic': 'Orlando',
        'Philadelphia 76ers': 'Philadelphia',
        'Phoenix Suns': 'Phoenix',
        'Portland Trail Blazers': 'Portland',
        'Sacramento Kings': 'Sacramento',
        'San Antonio Spurs': 'San Antonio',
        'Utah Jazz': 'Salt Lake City',
        'Washington Wizards': 'Washington',
        'Toronto Raptors': 'Toronto'
    }

    # Approximate city population data (U.S. Census + Canadian Census)
    city_populations = {
        'Atlanta': {2000: 416474, 2010: 420003, 2020: 498715},
        'Boston': {2000: 589141, 2010: 617594, 2020: 675647},
        'Brooklyn': {2000: 2465326, 2010: 2559903, 2020: 2648452},  # borough of NYC
        'Charlotte': {2000: 540828, 2010: 731424, 2020: 874579},
        'Chicago': {2000: 2896016, 2010: 2695598, 2020: 2746388},
        'Cleveland': {2000: 478403, 2010: 396815, 2020: 372624},
        'Dallas': {2000: 1188580, 2010: 1197816, 2020: 1304379},
        'Denver': {2000: 554636, 2010: 600158, 2020: 715522},
        'Detroit': {2000: 951270, 2010: 713777, 2020: 639111},
        'San Francisco': {2000: 776733, 2010: 805235, 2020: 873965},
        'Houston': {2000: 1953631, 2010: 2099451, 2020: 2304580},
        'Indianapolis': {2000: 781870, 2010: 820445, 2020: 887642},
        'Los Angeles': {2000: 3694820, 2010: 3792621, 2020: 3898747},
        'Memphis': {2000: 650100, 2010: 646889, 2020: 633104},
        'Miami': {2000: 362470, 2010: 399457, 2020: 442241},
        'Milwaukee': {2000: 596974, 2010: 594833, 2020: 577222},
        'Minneapolis': {2000: 382618, 2010: 382578, 2020: 429606},
        'New Orleans': {2000: 484674, 2010: 343829, 2020: 383997},
        'New York': {2000: 8008278, 2010: 8175133, 2020: 8804190},
        'Oklahoma City': {2000: 506132, 2010: 579999, 2020: 681054},
        'Orlando': {2000: 185951, 2010: 238300, 2020: 307573},
        'Philadelphia': {2000: 1517550, 2010: 1526006, 2020: 1603797},
        'Phoenix': {2000: 1321045, 2010: 1445632, 2020: 1608139},
        'Portland': {2000: 529121, 2010: 583776, 2020: 652503},
        'Sacramento': {2000: 407018, 2010: 466488, 2020: 524943},
        'San Antonio': {2000: 1144646, 2010: 1327407, 2020: 1434625},
        'Salt Lake City': {2000: 181743, 2010: 186440, 2020: 199723},
        'Washington': {2000: 572059, 2010: 601723, 2020: 689545},
        'Toronto': {2000: 2481494, 2010: 2615060, 2020: 2930000}
    }

    # Map U.S. census years to Canadian equivalents
    # toronto_year_map = {2000: 2001, 2010: 2011, 2020: 2021}
    #
    # years = [2000, 2010, 2020]
    #
    # for year in years:
    #     team_city_pop = []
    #
    #     for team, city in nba_cities.items():
    #         lookup_year = toronto_year_map.get(year, year) if city == 'Toronto' else year
    #
    #         if city not in city_populations:
    #             continue  # skip if data missing
    #
    #         pop = city_populations[city].get(lookup_year)
    #         if pop is not None:
    #             team_city_pop.append((team, city, pop))
    #
    #     # Sort descending by population
    #     team_city_pop.sort(key=lambda x: x[2], reverse=True)
    #
    #     print(f"\n🏙️ NBA Team City Population Rankings ({year}):")
    #     for rank, (team, city, pop) in enumerate(team_city_pop, 1):
    #         print(f"{rank:2d}. {team:<30} ({city}): {pop:,}")

    return pd.DataFrame(city_populations)

def get_average_draft_data():

    draft_data = DraftHistory().get_data_frames()[0]

    df = draft_data[['TEAM_CITY', 'TEAM_NAME', 'SEASON', 'OVERALL_PICK']].copy()
    # df['team_name'] = df['TEAM_CITY'] + ' ' + df['TEAM_NAME']


    summary_df = (
        df.groupby(['TEAM_NAME', 'SEASON'])
        .agg(
            number_of_picks=('OVERALL_PICK', 'count'),
            average_overall_pick=('OVERALL_PICK', 'mean')
        )
        .reset_index()
        .sort_values(['TEAM_NAME', 'SEASON'], ascending=[True, False])
    )
    summary_df['SEASON'] = summary_df['SEASON'].apply(lambda x: x + '-' + str(int(x) + 1))
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    pd.set_option('display.colheader_justify', 'center')

    #print(summary_df)
    #show(summary_df)

    return summary_df


def get_rest_days():
    filename = 'Data/Games.csv'  # CSV Name
    okc_games = []

    df = pd.read_csv(filename)

    df['gameDate'] = pd.to_datetime(df['gameDate'])

    # Data Frame
    home = df[['hometeamName', 'gameDate']].rename(columns={'hometeamName': 'Team'})
    away = df[['awayteamName', 'gameDate']].rename(columns={'awayteamName': 'Team'})
    all_games = pd.concat([home, away])

    all_games = all_games.sort_values(by=['Team', 'gameDate'])

    # Intervals
    all_games['RestDays'] = all_games.groupby('Team')['gameDate'].diff().dt.days

    output_path = 'Data/Team_RestDays.csv'
    all_games.to_csv(output_path, index=False)

    return all_games

def get_cleaned_games_with_winner_column():
    # Load your dataset
    df = pd.read_csv("Data/Games.csv")

    # Drop the columns you don't need
    columns_to_drop = ["arenaId", "homeTeamCity", "awayTeamCity","seriesgamenumber","gamelabel","gamesublabel","attendance","homescore","awayscore","gameid","gametype"]
    df = df.drop(columns=columns_to_drop, errors="ignore", axis=1)

    # Define a function to assign a season based on the game date
    def assign_season(date_str):
        # Make sure the date is parsed properly
        date = pd.to_datetime(date_str)
        year = date.year
        # NBA seasons start in the fall of one year and end in the next
        if date.month >= 10:  # October or later → start of a new season
            return f"{year}-{year + 1}"
        else:  # January to June → still part of the previous season
            return f"{year - 1}-{year}"

    # Apply the season function to create a new column
    df["season"] = df["gameDate"].apply(assign_season)

    # Save the cleaned version to a new file
    df.to_csv("games_cleaned.csv", index=False)

    #print("Columns dropped and 'season' column added successfully!")
    #print(df.head())


    # Standardize column names just in case (lowercase all)
    df.columns = df.columns.str.lower()

    # Convert winner column into 1 (home team) or 0 (away team)
    df["winner_binary"] = df.apply(
        lambda row: 1 if row["winner"] == row["hometeamid"] else 0, axis=1
    )

    # (Optional) drop the original winner column
    # df = df.drop(columns=["winner"])

    # Save the updated CSV
    df.to_csv("games_with_winner_binary.csv", index=False)

    #print("Converted 'winner' column to binary (1 = home win, 0 = away win).")
    #print(df[["hometeamname", "awayteamname", "winner", "winner_binary"]].head())

    #show (df)

    #print (df.info())
    return df


def get_teamaveragestatistics_from_year():

    df = pd.read_csv("Data/TeamStatistics.csv")

    # Convert gameDate to datetime
    df['gameDate'] = pd.to_datetime(df['gameDate'])

    # Optional: create a season column
    # Assuming NBA season starts in October and ends in June
    def get_season(date):
        if date.month >= 10:  # October or later
            return f"{date.year}-{date.year+1}"
        else:  # Jan-June
            return f"{date.year-1}-{date.year}"

    df['season'] = df['gameDate'].apply(get_season)

    # Stats to average
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
        "plusMinusPoints"
    ]

    # Group by season and team
    season_team_averages = df.groupby(["season", "teamName"])[stats].mean().reset_index()

    # Round for readability
    season_team_averages = season_team_averages.round(2)

    # Save to CSV
    season_team_averages.to_csv("nba_season_team_averages.csv", index=False)

    #print(season_team_averages)




    return season_team_averages

def get_bbr_winshares(season_end_year=2025):
    """Scrape Win Shares from Basketball Reference advanced stats page."""
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}_advanced.html"
    tables = pd.read_html(url)
    df = tables[0]
    df.rename(columns={'Team': 'TEAM_ABBREVIATION'}, inplace=True)
    return df


def get_all_winshares():
    for year in range(2000, 2026):
        print(f"Fetching Win Shares from Basketball Reference for {year} season...")

        # Fetch data
        ws_df = get_bbr_winshares(year)
        time.sleep(1)  # small delay to avoid rate limits if scraping

        ws_df["Season"]=str(year-1)+'-'+str(year)
        # Save individual season file
        file_name = f"nba_players_with_winshares_{year}.csv"
        ws_df.to_csv(file_name, index=False)

        print(f"✅ Done saving {file_name}")

    print("\n🎯 All seasons (2000–2025) have been processed and saved.")

    all_data = pd.concat(
        [pd.read_csv(f"nba_players_with_winshares_{year}.csv") for year in range(2000, 2026)],
        ignore_index=True
    )

    all_data.to_csv("nba_players_with_winshares_all_2000_2025.csv", index=False)
    print("📁 Combined file saved: nba_players_with_winshares_all_2000_2025.csv")



