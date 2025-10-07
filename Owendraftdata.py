import pandas as pd
from nba_api.stats.endpoints import DraftHistory
from pandasgui import show


def get_all_drafts(start_year, end_year):


    # Pull the full draft history (all seasons)
    draft_history = DraftHistory()

    # Convert to DataFrame
    draft_df = draft_history.get_data_frames()[0]

    # Filter the DataFrame for seasons 1947 to 2025
    draft_all_years = draft_df[(draft_df['SEASON'].astype(int) >= start_year) &
                                (draft_df['SEASON'].astype(int) <= end_year)]

    return draft_all_years






