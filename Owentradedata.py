from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static import teams
import pandas as pd
import time
from tqdm import tqdm
import threading
import queue
import os
import datetime
import sys

# === CONFIG ===
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "inferred_trades")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "nba_inferred_trades.csv")
START_YEAR = 1970
END_YEAR = 2026
SLEEP_TIME = 0.6
NUM_THREADS = 5

# === Ensure output directory exists ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Load existing data if it exists ===
if os.path.exists(OUTPUT_FILE):
    trades_df = pd.read_csv(OUTPUT_FILE)
    print(f"✅ Loaded existing file with {len(trades_df)} rows: {OUTPUT_FILE}")
else:
    trades_df = pd.DataFrame(columns=["Player", "From", "To", "Season"])
    print(f"🆕 Creating new trade file: {OUTPUT_FILE}")

# === Build queue of all team-year combos ===
all_teams = teams.get_teams()
task_queue = queue.Queue()
for season in range(START_YEAR, END_YEAR + 1):
    for team in all_teams:
        task_queue.put((season, team))

lock = threading.Lock()
total_tasks = task_queue.qsize()
pbar = tqdm(total=total_tasks, desc="Fetching NBA trade data", unit="calls")

def fetch_trades():
    global trades_df
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
            print(f"⚠️ Error fetching {team_name} {season}: {e}")
        finally:
            time.sleep(SLEEP_TIME)
            with lock:
                pbar.update(1)

    # Merge and write
    if local_trades:
        local_df = pd.DataFrame(local_trades)
        with lock:
            trades_df = pd.concat([trades_df, local_df], ignore_index=True)
            trades_df.drop_duplicates(subset=["Player", "Season"], keep="last", inplace=True)
            trades_df.sort_values(by="Season", ascending=False, inplace=True)
            try:
                trades_df.to_csv(OUTPUT_FILE, index=False)
                print(f"💾 Saved progress ({len(trades_df)} rows) → {OUTPUT_FILE}")
            except Exception as e:
                print(f"❌ Could not save CSV: {e}")
                sys.exit(1)

# === Run threads ===
start_time = time.time()
threads = []
for _ in range(NUM_THREADS):
    t = threading.Thread(target=fetch_trades)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

pbar.close()

# === Final write + summary ===
try:
    trades_df.sort_values(by="Season", ascending=False, inplace=True)
    trades_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Final CSV saved successfully at:\n{OUTPUT_FILE}")
except Exception as e:
    print(f"❌ Final save failed: {e}")

elapsed = time.time() - start_time
print(f"⏱ Total runtime: {str(datetime.timedelta(seconds=int(elapsed)))}")

# === Preview first 10 rows ===
print("\nFirst 10 trades:")
print(trades_df.head(10))

# === Optional: Summary count per season ===
print("\nNumber of trades per season:")
print(trades_df.groupby("Season").size().sort_index(ascending=False))
