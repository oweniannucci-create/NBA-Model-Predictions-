import pandas as pd

# Load your data
df = pd.read_csv("Data/TeamStatistics.csv")


numeric_cols = df.select_dtypes(include="number").columns

# Group by teamName and calculate averages
team_averages = df.groupby("teamName")[numeric_cols].mean().round(2)

print(team_averages.head())



