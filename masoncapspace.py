import requests
import pandas as pd

teams = [
    {"team": "Atlanta Hawks",        "city": "Atlanta, GA"},
    {"team": "Boston Celtics",       "city": "Boston, MA"},
    {"team": "Charlotte Hornets",    "city": "Charlotte, NC"},
    # ... include all 29 teams ...
]

years = [2000, 2010, 2020]

# Define a function to get city population from Census API
def get_population(city_name, state_code, year):
    """
    Fetches the place-population from the Census API for the given city, state and year.
    You will need to map city_name → place FIPS code (or a lookup) in a real implementation.
    """
    if year == 2010:
        # Example: Summary File 2 for 2010: variable HCT001001 is total population
        url = f"https://api.census.gov/data/2010/dec/sf2?get=HCT001001,NAME&for=place:*&in=state:{state_code}"
        resp = requests.get(url)
        data = resp.json()
        for row in data[1:]:
            # row format: [pop, NAME, state, place]
            if row[1].startswith(city_name):
                return int(row[0])
        return None

    elif year == 2020:
        # Example: Decennial Census 2020 Demographic Profile (DP) dataset
        # variable P1_001N gives total population (check the exact variable in docs)
        url = f"https://api.census.gov/data/2020/dec/pl?get=P1_001N,NAME&for=place:*&in=state:{state_code}"
        resp = requests.get(url)
        data = resp.json()
        for row in data[1:]:
            if row[1].startswith(city_name):
                return int(row[0])
        return None

    elif year == 2000:
        # For 2000 you might use Summary File 1 for year 2000, variable P001001
        url = f"https://api.census.gov/data/2000/dec/sf1?get=P001001,NAME&for=place:*&in=state:{state_code}"
        resp = requests.get(url)
        data = resp.json()
        for row in data[1:]:
            if row[1].startswith(city_name):
                return int(row[0])
        return None

    else:
        raise ValueError("Year not supported")

# Example: map each city to its state FIPS code
state_fips = {
    "GA": "13", "MA": "25", "NC": "37",
    # ... all states ...
}

rows = []
for t in teams:
    city = t["city"].split(",")[0]
    state = t["city"].split(",")[1].strip()
    for yr in years:
        pop = get_population(city, state_fips[state], yr)
        rows.append({"team": t["team"], "city": t["city"], "year": yr, "population": pop})

df = pd.DataFrame(rows)

for yr in years:
    print(f"\n--- Census Year {yr} ---")
    dfy = df[df["year"] == yr].dropna(subset=["population"]).sort_values(by="population", ascending=False)
    dfy["rank"] = range(1, len(dfy)+1)
    print(dfy[["rank","team","city","population"]].to_string(index=False))

