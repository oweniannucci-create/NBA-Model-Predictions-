from nba_api.stats.endpoints import commonteamroster, teamdetails
from nba_api.stats.static import teams
import pandas as pd
import time

all_teams = teams.get_teams()
all_data = []

for team in all_teams:
    team_id = team["id"]
    team_name = team["full_name"]
    print(f"📊 Pulling {team_name}...")

    for season in range(2004, 2014):
        try:
            roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=f"{season}-{str(season+1)[2:]}")
            roster_df = roster.get_data_frames()[0]
            roster_df["Team"] = team_name
            roster_df["Season"] = season
            all_data.append(roster_df)
            time.sleep(0.6)  # Avoid rate limit
        except Exception as e:
            print(f"⚠️ {team_name} {season}: {e}")

# Combine all into one big dataframe
all_trades_df = pd.concat(all_data, ignore_index=True)
all_trades_df.to_csv("nba_rosters_2015_to_2024.csv", index=False)

print("\n✅ Saved all team rosters to nba_rosters_2015_to_2024.csv")


# Detect players who switched teams
trades = []

for player, group in all_trades_df.groupby("PLAYER"):
    if group["Team"].nunique() > 1:
        sorted_teams = group.sort_values("Season")[["Season", "Team"]].drop_duplicates()
        for i in range(1, len(sorted_teams)):
            prev_team = sorted_teams.iloc[i - 1]["Team"]
            new_team = sorted_teams.iloc[i]["Team"]
            trades.append({
                "Player": player,
                "From": prev_team,
                "To": new_team,
                "Season": sorted_teams.iloc[i]["Season"]
            })

pd.DataFrame(trades).to_csv("nba_inferred_trades.csv", index=False)
print(f"💾 Inferred {len(trades)} trades saved to nba_inferred_trades.csv")
