import pandas as pd
from pandasgui import show


def get_team_rest_days(filename='Data/Games.csv'):



    df = pd.read_csv(filename)
    df['gameDate'] = pd.to_datetime(df['gameDate'])


    home = df[['hometeamName', 'gameDate']].rename(columns={'hometeamName': 'Team'})
    away = df[['awayteamName', 'gameDate']].rename(columns={'awayteamName': 'Team'})
    all_games = pd.concat([home, away])


    all_games = all_games.sort_values(by=['Team', 'gameDate'])


    all_games['RestDays'] = all_games.groupby('Team')['gameDate'].diff().dt.days


    all_games.to_csv('Data/Team_RestDays.csv', index=False)

    #DataFrame
    return all_games



if __name__ == "__main__":
    team_rest_df = get_team_rest_days()
    print(team_rest_df.head())
    show(team_rest_df)


#Use

#from RestDate import get_team_rest_days
#df_rest = get_team_rest_days()
#print(df_rest)
