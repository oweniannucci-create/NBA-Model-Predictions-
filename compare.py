import pandas as pd

# 1. Load the CSV files
# Replace these with the actual paths to your CSV files
predictions_df = pd.read_csv('2025-2026-predictions.csv')
results_df = pd.read_csv('nba_home_away_results_2025-26.csv')

# 2. Define the exact column names from your CSV files
model_1_col = 'home_team_win_pred_nn'       # Column with Model 1 predictions (e.g., predicted winning team)
model_2_col = 'home_team_win_pred_xgb'       # Column with Model 2 predictions
actual_result_col = 'HOME_WIN'
game_id_col = 'gamedate'
# Column with the actual game results

# 3. Merge the datasets to ensure predictions are aligned with the correct games
# We use an inner join to only compare games present in both files
merged_df = pd.merge(
    predictions_df[[game_id_col, model_1_col, model_2_col]],
    results_df[[game_id_col, actual_result_col]],
    on=game_id_col,
    how='inner'
)

# 4. Calculate accuracy
# Compares model predictions to the actual results and calculates the mean (which equals the accuracy percentage)
total_games = len(merged_df)
model_1_accuracy = (merged_df[model_1_col] == merged_df[actual_result_col]).mean() * 100
model_2_accuracy = (merged_df[model_2_col] == merged_df[actual_result_col]).mean() * 100

# 5. Display the results
print(f"Total games evaluated: {total_games}")
print(f"Our NN Predictions: {model_1_accuracy:.2f}%")
print(f"XGB Predictions: {model_2_accuracy:.2f}%")
