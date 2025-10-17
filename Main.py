import DataFetcher


games_df = DataFetcher.get_cleaned_games_with_winner_column()
stats_df = DataFetcher.get_teamaveragestatistics_from_year()
draft_df = DataFetcher.get_average_draft_data()

print(games_df.info())
print(stats_df.info())
print(draft_df.info())

