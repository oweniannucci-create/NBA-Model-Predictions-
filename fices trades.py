import pandas as pd

# Step 1: Load both CSV files
df1 = pd.read_csv("/Users/owenray/Documents/GitHub/NBA-Model-Predictions-/nba_inferred_trades_fixed.csv")
df2 = pd.read_csv("/Users/owenray/Documents/GitHub/NBA-Model-Predictions-/nba_inferred_trades.csv")

# Step 2: Combine the two datasets
combined = pd.concat([df1, df2], ignore_index=True)

# Step 3: Sort by Player and Season
combined_sorted = combined.sort_values(by=["Player", "Season"])

# Step 4: Save the sorted combined data
output_file = "/Users/owenray/Documents/GitHub/NBA-Model-Predictions-/nba_trades_combined_sorted.csv"
combined_sorted.to_csv(output_file, index=False)

print("✅ Combined and sorted CSV saved as nba_trades_combined_sorted.csv")
