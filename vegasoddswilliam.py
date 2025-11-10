import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_preseason_odds(year):
    """
    Fetch the preseason odds table for the given NBA season end-year,
    e.g. year = 2024 → URL ends with NBA_2024_preseason_odds.html
    """
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_preseason_odds.html"
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Warning: Failed to fetch {url} (status {resp.status_code})")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the table — inspect the page to get correct selector
    table = soup.find("table", {"id": "preseason_odds"})  # guess: id = preseason_odds
    if table is None:
        print(f"Warning: Table not found for year {year}")
        return None

    # Extract header
    cols = [th.get_text().strip() for th in table.find("thead").find_all("th")]
    # Extract rows
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        if tr.get("class") and "thead" in tr.get("class"):
            continue  # skip header rows inside body
        cells = [td.get_text().strip() for td in tr.find_all(["th","td"])]
        if not cells:
            continue
        rows.append(cells)

    # Build DataFrame
    df = pd.DataFrame(rows, columns=cols)
    df["Season_End_Year"] = year
    return df

def scrape_all(years, pause_sec=1.0):
    all_dfs = []
    for y in years:
        print(f"Fetching year {y} …")
        df = fetch_preseason_odds(y)
        if df is not None:
            all_dfs.append(df)
        time.sleep(pause_sec)
    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
    else:
        combined = pd.DataFrame()
    return combined

if __name__ == "__main__":
    years = list(range(2000, 2026))
    df_all = scrape_all(years, pause_sec=2.0)
    if not df_all.empty:
        df_all.to_csv("nba_preseason_odds_2000_2025.csv", index=False)
        print("✅ Saved CSV with rows:", len(df_all))
    else:
        print("⚠️ No data fetched.")
