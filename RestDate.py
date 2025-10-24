import csv
import pandas as pd
from pandasgui import show

filename = 'Data/Games.csv'  #CSV Name
okc_games = []

df = pd.read_csv(filename)

df['gameDate'] = pd.to_datetime(df['gameDate'])

# Data Frame
home = df[['hometeamName', 'gameDate']].rename(columns={'hometeamName': 'Team'})
away = df[['awayteamName', 'gameDate']].rename(columns={'awayteamName': 'Team'})
all_games = pd.concat([home, away])

all_games = all_games.sort_values(by=['Team', 'gameDate'])

# Intervals
all_games['RestDays'] = all_games.groupby('Team')['gameDate'].diff().dt.days

print(all_games)
show(all_games)
# all_games.to_csv('Team_RestDays.csv', index=False)
