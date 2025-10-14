import pandas as pd
from pandasgui import show
# Load your dataset
df = pd.read_csv("Data/Games.csv")

# Drop the columns you don't need
columns_to_drop = ["arenaId", "homeTeamCity", "awayTeamCity"]
df = df.drop(columns=columns_to_drop, errors="ignore")

# Define a function to assign a season based on the game date
def assign_season(date_str):
    # Make sure the date is parsed properly
    date = pd.to_datetime(date_str)
    year = date.year
    # NBA seasons start in the fall of one year and end in the next
    if date.month >= 10:  # October or later → start of a new season
        return f"{year}-{year + 1}"
    else:  # January to June → still part of the previous season
        return f"{year - 1}-{year}"

# Apply the season function to create a new column
df["season"] = df["gameDate"].apply(assign_season)

# Save the cleaned version to a new file
df.to_csv("games_cleaned.csv", index=False)

print("Columns dropped and 'season' column added successfully!")
print(df.head())


# Standardize column names just in case (lowercase all)
df.columns = df.columns.str.lower()

# Convert winner column into 1 (home team) or 0 (away team)
df["winner_binary"] = df.apply(
    lambda row: 1 if row["winner"] == row["hometeamid"] else 0, axis=1
)

# (Optional) drop the original winner column
# df = df.drop(columns=["winner"])

# Save the updated CSV
df.to_csv("games_with_winner_binary.csv", index=False)

print("Converted 'winner' column to binary (1 = home win, 0 = away win).")
print(df[["hometeamname", "awayteamname", "winner", "winner_binary"]].head())

show (df)

print (df.info())