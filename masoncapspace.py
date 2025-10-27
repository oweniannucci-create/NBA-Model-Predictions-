import pandas as pd

# List of the (circa 2000) NBA teams and their home cities
teams = [
    {"team": "Atlanta Hawks",          "city": "Atlanta, GA"},
    {"team": "Boston Celtics",         "city": "Boston, MA"},
    {"team": "Charlotte Hornets",      "city": "Charlotte, NC"},
    {"team": "Chicago Bulls",          "city": "Chicago, IL"},
    {"team": "Cleveland Cavaliers",    "city": "Cleveland, OH"},
    {"team": "Dallas Mavericks",       "city": "Dallas, TX"},
    {"team": "Denver Nuggets",         "city": "Denver, CO"},
    {"team": "Detroit Pistons",        "city": "Detroit, MI"},
    {"team": "Golden State Warriors",  "city": "San Francisco, CA"},
    {"team": "Houston Rockets",        "city": "Houston, TX"},
    {"team": "Indiana Pacers",         "city": "Indianapolis, IN"},
    {"team": "Los Angeles Lakers",     "city": "Los Angeles, CA"},
    {"team": "Los Angeles Clippers",   "city": "Los Angeles, CA"},
    {"team": "Memphis Grizzlies",      "city": "Memphis, TN"},
    {"team": "Miami Heat",             "city": "Miami, FL"},
    {"team": "Milwaukee Bucks",        "city": "Milwaukee, WI"},
    {"team": "Minnesota Timberwolves", "city": "Minneapolis, MN"},
    {"team": "New Jersey Nets",        "city": "Newark, NJ"},
    {"team": "New York Knicks",        "city": "New York, NY"},
    {"team": "Orlando Magic",          "city": "Orlando, FL"},
    {"team": "Philadelphia 76ers",     "city": "Philadelphia, PA"},
    {"team": "Phoenix Suns",           "city": "Phoenix, AZ"},
    {"team": "Portland Trail Blazers", "city": "Portland, OR"},
    {"team": "Sacramento Kings",       "city": "Sacramento, CA"},
    {"team": "San Antonio Spurs",      "city": "San Antonio, TX"},
    {"team": "Seattle SuperSonics",    "city": "Seattle, WA"},
    {"team": "Toronto Raptors",        "city": "Toronto, ON"},  # Note: Canadian city — you may exclude if US only
    {"team": "Utah Jazz",              "city": "Salt Lake City, UT"},
    {"team": "Washington Wizards",     "city": "Washington, DC"},
]

years = [2000, 2010, 2020]

# Placeholder dictionary: city → {year: population, …}
city_pop = {
    # Example entries (you must fill out for each city and all years)
    "New York, NY":      {2000: 8008278, 2010: 8175133, 2020: None},
    "Los Angeles, CA":   {2000: 3694820, 2010: 3792621, 2020: None},
    "Chicago, IL":       {2000: 2896016, 2010: 2695598, 2020: None},
    # … continue for all cities …
}

# Build DataFrame
rows = []
for t in teams:
    city = t["city"]
    for yr in years:
        pop = city_pop.get(city, {}).get(yr, None)
        rows.append({"team": t["team"], "city": city, "year": yr, "population": pop})

df = pd.DataFrame(rows)

# For each year, rank teams by population descending
for yr in years:
    print(f"\n--- Census Year {yr} ---")
    df_year = df[df["year"] == yr].copy()
    df_year = df_year.dropna(subset=["population"])
    df_year = df_year.sort_values(by="population", ascending=False)
    df_year["rank"] = range(1, len(df_year) + 1)
    print(df_year[["rank", "team", "city", "population"]].to_string(index=False))

