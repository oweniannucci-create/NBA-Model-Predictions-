from pandasgui import show
import pandas as pd
import DataFetcher

current_games = pd.read_csv("nba_schedule_2025_26.csv")
games_df = DataFetcher.get_cleaned_games_with_winner_column()
all_games = pd.concat([games_df, current_games], ignore_index=True)

show(all_games)