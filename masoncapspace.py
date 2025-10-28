import pandas as pd

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
    'Toronto': {2001: 2481494, 2011: 2615060, 2021: 2930000}
}

# Map U.S. census years to Canadian equivalents
toronto_year_map = {2000: 2001, 2010: 2011, 2020: 2021}

years = [2000, 2010, 2020]

for year in years:
    team_city_pop = []

    for team, city in nba_cities.items():
        lookup_year = toronto_year_map.get(year, year) if city == 'Toronto' else year

        if city not in city_populations:
            continue  # skip if data missing

        pop = city_populations[city].get(lookup_year)
        if pop is not None:
            team_city_pop.append((team, city, pop))

    # Sort descending by population
    team_city_pop.sort(key=lambda x: x[2], reverse=True)

    print(f"\n🏙️ NBA Team City Population Rankings ({year}):")
    for rank, (team, city, pop) in enumerate(team_city_pop, 1):
        print(f"{rank:2d}. {team:<30} ({city}): {pop:,}")

