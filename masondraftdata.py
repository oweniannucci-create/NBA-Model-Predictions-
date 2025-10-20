# import pandas as pd
from nba_api.stats.endpoints import DraftHistory
import pandas as pd
from pandasgui import show

def get_average_draft_data():

    draft_data = DraftHistory().get_data_frames()[0]

    df = draft_data[['TEAM_CITY', 'TEAM_NAME', 'SEASON', 'OVERALL_PICK']].copy()
    # df['team_name'] = df['TEAM_CITY'] + ' ' + df['TEAM_NAME']


    summary_df = (
        df.groupby(['TEAM_NAME', 'SEASON'])
        .agg(
            number_of_picks=('OVERALL_PICK', 'count'),
            average_overall_pick=('OVERALL_PICK', 'mean')
        )
        .reset_index()
        .sort_values(['TEAM_NAME','SEASON'], ascending=[True, False])
    )
    summary_df['SEASON'] = summary_df['SEASON'].apply(lambda x: x + '-' + str(int(x) + 1))
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    pd.set_option('display.colheader_justify', 'center')

    #print(summary_df)
    #show(summary_df)

    return summary_df

#get_average_draft_data()


