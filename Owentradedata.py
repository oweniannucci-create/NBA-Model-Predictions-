from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static import teams
import pandas as pd
import time
from tqdm import tqdm
import threading
import queue
import os
import datetime

# === CONFIG ===
OUTPUT_FILE = "nba_inferred_trades.csv"
START_YEAR = 1960
END_YEAR = 2026
SLEEP_TIME = 0.6  # seconds between API calls per thread
NUM_THREADS = 5   # number of threads to run in parallel

# === Load existing trades CSV if exists (auto-resume) ===
if os.path.exists(OUTPUT_FILE):
    trades_df = pd.read_csv(OUTPUT_FILE)
    print(f"✅ Loaded existing trade file with {len(trades_df)} rows.")
else:
    trades_df = pd.DataFrame()

# === Queue for thread tasks (season, team) ===
all_teams = teams.get_teams()
task_queue = queue.Queue()
for season in range(START_YEAR, END_YEAR + 1):
    for team in all_teams:
        task_queue.put((season, team))

# === Lock for safely updating main dataframe and progress bar ===
lock = threading.Lock()

# === Progress bar setup ===
total_tasks = task_queue.qsize()
pbar = tqdm(total=total_tasks, desc="Fetching NBA trade data", unit="calls")

# === Thread function ===
def fetch_trades():
    global trades_df  # must be first line in the function
    local_trades = []

    while not task_queue.empty():
        try:
            season, team = task_queue.get_nowait()
        except queue.Empty:
            break

        team_id = team["id"]
        team_name = team["full_name"]

        try:
            roster = commonteamroster.CommonTeamRoster(
                team_id=team_id,
                season=f"{season}-{str(season+1)[2:]}"
            )
            roster_df = roster.get_data_frames()[0]
            roster_df["Team"] = team_name
            roster_df["Season"] = season

            # Detect trades
            for player, group in roster_df.groupby("PLAYER"):
                prev_entries = trades_df[trades_df["Player"] == player]
                if prev_entries.empty:
                    continue
                prev_team = prev_entries.iloc[-1]["To"]
                current_team = group["Team"].iloc[0]
                if prev_team != current_team:
                    local_trades.append({
                        "Player": player,
                        "From": prev_team,
                        "To": current_team,
                        "Season": season
                    })

        except Exception as e:
            print(f"⚠️ {team_name} {season}: {e}")
        finally:
            time.sleep(SLEEP_TIME)
            with lock:
                pbar.update(1)

    # Merge local trades into main dataframe safely
    if local_trades:
        local_df = pd.DataFrame(local_trades)
        with lock:
            trades_df = pd.concat([trades_df, local_df], ignore_index=True)
            trades_df.to_csv(OUTPUT_FILE, index=False)

# === Start timer ===
start_time = time.time()

# === Start threads ===
threads = []
for _ in range(NUM_THREADS):
    t = threading.Thread(target=fetch_trades)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

pbar.close()

# === Done ===
elapsed = time.time() - start_time
print(f"\n✅ All trade data saved to {OUTPUT_FILE}")
print(f"⏱ Total runtime: {str(datetime.timedelta(seconds=int(elapsed)))}")
