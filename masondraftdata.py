import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

def get_salary_cap_history():
    """Fetches NBA salary-cap history from Basketball Reference (works without 403)."""
    url = "https://www.basketball-reference.com/contracts/salary-cap-history.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "salary_cap_history"})
    df = pd.read_html(StringIO(str(table)))[0]
    df.columns = ["Season", "Salary Cap", "Luxury Tax", "Apron"]

    # Clean up
    for c in ["Salary Cap", "Luxury Tax", "Apron"]:
        df[c] = df[c].replace({r"[\$,]": ""}, regex=True).astype(float)

    df["Year"] = df["Season"].str[:4].astype(int)
    df = df[df["Year"] >= 2011].reset_index(drop=True)
    return df[["Year", "Salary Cap", "Luxury Tax"]]


def fake_team_salary_data(years, teams):
    """Simulates team salary commitments so code runs right now."""
    import numpy as np
    data = []
    for y in years:
        for t in teams:
            team_salary = np.random.uniform(80_000_000, 160_000_000)  # fake number
            data.append([y, t, team_salary])
    return pd.DataFrame(data, columns=["Year", "Team", "Team Salary"])


def combine_cap_space(cap_df, team_df):
    """Compute each team's cap space = salary cap - team salary."""
    df = pd.merge(team_df, cap_df, on="Year", how="left")
    df["Cap Space"] = df["Salary Cap"] - df["Team Salary"]
    return df


def main():
    cap_df = get_salary_cap_history()
    teams = [
        "Lakers", "Celtics", "Bulls", "Warriors", "Heat", "Nets",
        "Mavericks", "Knicks", "76ers", "Suns"
    ]

    # Create example team salary data (replace later with real data)
    team_df = fake_team_salary_data(cap_df["Year"].tolist(), teams)

    full_df = combine_cap_space(cap_df, team_df)

    print(full_df.head(20))
    full_df.to_csv("nba_cap_space_2011_2025.csv", index=False)
    print("✅ Saved nba_cap_space_2011_2025.csv")


if __name__ == "__main__":
    main()
