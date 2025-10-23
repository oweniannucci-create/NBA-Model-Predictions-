import pandas as pd

# Wikipedia page with NBA All-Star rosters
url = "https://en.wikipedia.org/wiki/NBA_All-Star_Game"

# Read all tables from the page
tables = pd.read_html(url)

allstars_list = []

# Loop through tables to find yearly All-Star rosters
for table in tables:
    # Only look at tables that contain a 'Starters' or 'Reserves' column
    if any(col in table.columns for col in ['Starters', 'Reserves']):
        # Get the year from the first column if possible
        year = table.iloc[0, 0]
        # Some tables have multiple rows per year, flatten them
        starters = table['Starters'].dropna().tolist()
        reserves = table['Reserves'].dropna().tolist()
        for player in starters + reserves:
            allstars_list.append({'Year': year, 'Player': player})

# Convert to DataFrame
df_allstars = pd.DataFrame(allstars_list)

# Filter years 2000–2026
df_allstars = df_allstars[df_allstars['Year'].astype(str).str[:4].astype(int).between(2000, 2026)]

# Save to CSV
df_allstars.to_csv("nba_allstars_2000_2026.csv", index=False)
print("✅ Saved All-Star players 2000-2026 to nba_allstars_2000_2026.csv")
