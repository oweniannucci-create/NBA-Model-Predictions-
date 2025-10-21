import pandas as pd

# Step 1: Read both files
df1 = pd.read_csv('Nba_inferred_trades.csv')
df2 = pd.read_csv('nba_inferred_trades.csv')

# Step 2: Combine
combined = pd.concat([df1, df2], ignore_index=True)

# Step 3: Sort by player and season
combined_sorted = combined.sort_values(by=['Player', 'Season'])

# Step 4: Save to new CSV
combined_sorted.to_csv('nba_trades_combined_sorted.csv', index=False)

print("✅ Combined and sorted CSV saved as 'nba_trades_combined_sorted.csv'")
