import pandas as pd

# === 1. Load your CSV ===
# Make sure this matches your actual file name
df = pd.read_csv('nba_trades_combined_sorted.csv')

# === 2. Rename columns for consistency ===
df = df.rename(columns={'Season': 'year', 'To': 'team', 'Player': 'player'})

# === 3. Keep only the relevant columns ===
df = df[['year', 'team', 'player']]

# === 4. Sort the data ===
df = df.sort_values(by=['year', 'team', 'player']).reset_index(drop=True)

# === 5. Save the final sorted roster to a single CSV ===
df.to_csv('nba_rosters_sorted.csv', index=False)

print("✅ All data sorted and saved as 'nba_rosters_sorted.csv' with columns: year, team, player")
