# import pandas as pd
from pandasgui import show
import pandas as pd
from nba_api.stats.endpoints import DraftHistory

def get_average_draft_data():

    draft_data = DraftHistory().get_data_frames()[0]

    df = draft_data[['TEAM_CITY', 'TEAM_NAME', 'season', 'OVERALL_PICK']].copy()
    df['team_name'] = df['TEAM_CITY'] + ' ' + df['TEAM_NAME']


    summary_df = (
        df.groupby(['team_name', 'season'])
        .agg(
            number_of_picks=('OVERALL_PICK', 'count'),
            average_overall_pick=('OVERALL_PICK', 'mean')
        )
        .reset_index()
        .sort_values(['team_name', 'season'], ascending=[True, False])
    )

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    pd.set_option('display.colheader_justify', 'center')

    #print(summary_df)
    show(summary_df)

    return summary_df


get_average_draft_data()


