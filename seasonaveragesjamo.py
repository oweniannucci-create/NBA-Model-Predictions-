import pandas as pd

# Load the CSV with season stats for multiple teams
df = pd.read_csv("Data/TeamStatistics.csv")
# Example columns: Season, Team, Wins, Losses, Points, Assists, Steals, 3P%

team_name = "Pacers"
team_df = df[df["teamName"] == team_name]

print(f"{"Pacers"} season stats preview:")
print(team_df.head())

# Calculate averages for numeric stats
average_stats = team_df.mean(numeric_only=True)

# Print out averages
print(f"\nAverage stats per season for {team_name}:")
print(average_stats)