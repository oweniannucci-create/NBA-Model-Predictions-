import pandas as pd
from nba_api.stats.endpoints import DraftHistory
from pandasgui import show

# Pull the full draft history (all seasons)
draft_history = DraftHistory()

# Convert to DataFrame
draft_df = draft_history.get_data_frames()[0]

# Filter the DataFrame for seasons 1947 to 2025
draft_all_years = draft_df[(draft_df['SEASON'].astype(int) >= 1957) &
                            (draft_df['SEASON'].astype(int) <= 2025)]



 #Check the first few rows
print(draft_all_years.head())
show(draft_all_years)