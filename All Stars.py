import pandas as pd
import requests

start_year = 2000
end_year = 2025
team_year_counts = {}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                  'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                  'Chrome/116.0.0.0 Safari/537.36'
}

for year in range(start_year, end_year + 1):
    url = f'https://www.basketball-reference.com/allstar/NBA_{year}.html'
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(f"❌ Could not fetch {year} (status {res.status_code})")
        continue

    tables = pd.read_html(res.text)

    # Usually first 2 tables are East/West All-Stars
    for table in tables[:2]:
        for _, row in table.iterrows():
            team = row['Tm'] if 'Tm' in row else row.get('Team', 'Unknown')
            if pd.isna(team):
                continue
            if year not in team_year_counts:
                team_year_counts[year] = {}
            if team not in team_year_counts[year]:
                team_year_counts[year][team] = 0
            team_year_counts[year][team] += 1

# Only proceed if we have data
if not team_year_counts:
    print("❌ No All-Star data fetched. Cannot create CSV.")
else:
    rows = []
    for year in sorted(team_year_counts.keys(), reverse=True):
        for team, count in team_year_counts[year].items():
            rows.append({'Year': year, 'Team': team, 'AllStar_Count': count})

    df = pd.DataFrame(rows)
    df = df.sort_values(by=['Year', 'Team'], ascending=[False, True])
    df.to_csv('nba_allstars_2000_2025_counts.csv', index=False)
    print("✅ Saved All-Star counts per team/year to nba_allstars_2000_2025_counts.csv")
