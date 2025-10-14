def build_nba_prediction_model():
    import pandas as pd
    from pandasgui import show
    from nba_api.stats.endpoints import DraftHistory
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, classification_report

    # ===================== 1️⃣ LOAD AND CLEAN GAME DATA =====================
    df_games = pd.read_csv("Data/Games.csv")

    # Drop unnecessary columns
    columns_to_drop = ["arenaId", "homeTeamCity", "awayTeamCity"]
    df_games = df_games.drop(columns=columns_to_drop, errors="ignore")

    # Assign season based on gameDate
    def assign_season(date_str):
        date = pd.to_datetime(date_str)
        year = date.year
        if date.month >= 10:
            return f"{year}-{year + 1}"
        else:
            return f"{year - 1}-{year}"

    df_games["season"] = df_games["gameDate"].apply(assign_season)

    # Convert winner column into binary (1 = home win, 0 = away win)
    df_games["winner_binary"] = df_games.apply(
        lambda row: 1 if row["winner"] == row["homeTeamId"] else 0, axis=1
    )

    # ===================== 2️⃣ LOAD AND AVERAGE TEAM STATISTICS =====================
    df_stats = pd.read_csv("Data/TeamStatistics.csv")

    df_stats["gameDate"] = pd.to_datetime(df_stats["gameDate"])

    def get_season(date):
        if date.month >= 10:
            return f"{date.year}-{date.year+1}"
        else:
            return f"{date.year-1}-{date.year}"

    df_stats["season"] = df_stats["gameDate"].apply(get_season)

    # Stats to average
    stats = [
        "teamScore",
        "assists",
        "reboundsDefensive",
        "reboundsOffensive",
        "reboundsTotal",
        "steals",
        "blocks",
        "turnovers",
        "foulsPersonal",
        "fieldGoalsMade",
        "fieldGoalsAttempted",
        "fieldGoalsPercentage",
        "threePointersMade",
        "threePointersAttempted",
        "threePointersPercentage",
        "freeThrowsMade",
        "freeThrowsAttempted",
        "freeThrowsPercentage",
        "plusMinusPoints",
    ]

    season_team_averages = (
        df_stats.groupby(["season", "teamName"])[stats]
        .mean()
        .reset_index()
        .round(2)
    )

    # ===================== 3️⃣ LOAD DRAFT DATA =====================
    draft_data = DraftHistory().get_data_frames()[0]
    df_draft = draft_data[["TEAM_CITY", "TEAM_NAME", "SEASON", "OVERALL_PICK"]].copy()
    df_draft["team_name"] = df_draft["TEAM_CITY"] + " " + df_draft["TEAM_NAME"]
    df_draft["draft_year"] = df_draft["SEASON"]

    draft_summary = (
        df_draft.groupby(["team_name", "draft_year"])
        .agg(
            number_of_picks=("OVERALL_PICK", "count"),
            average_overall_pick=("OVERALL_PICK", "mean"),
        )
        .reset_index()
    )

    # ===================== 4️⃣ MERGE EVERYTHING =====================

    # Merge home team stats
    merged = df_games.merge(
        season_team_averages,
        left_on=["season", "homeTeamName"],
        right_on=["season", "teamName"],
        how="left",
        suffixes=("", "_home"),
    )

    # Merge away team stats
    merged = merged.merge(
        season_team_averages,
        left_on=["season", "awayTeamName"],
        right_on=["season", "teamName"],
        how="left",
        suffixes=("_home", "_away"),
    )

    # Merge draft data for both teams
    merged = merged.merge(
        draft_summary,
        left_on=["homeTeamName", "season"],
        right_on=["team_name", "draft_year"],
        how="left",
        suffixes=("", "_home_draft"),
    )

    merged = merged.merge(
        draft_summary,
        left_on=["awayTeamName", "season"],
        right_on=["team_name", "draft_year"],
        how="left",
        suffixes=("_home_draft", "_away_draft"),
    )

    # ===================== 5️⃣ TRAIN PREDICTION MODEL =====================
    # Select features (home vs away stat difference)
    merged = merged.dropna(subset=["winner_binary"])

    # Create features: differences between home and away stats
    features = []
    for stat in stats:
        merged[f"diff_{stat}"] = (
            merged[f"{stat}_home"] - merged[f"{stat}_away"]
        )
        features.append(f"diff_{stat}")

    # Add draft differences if available
    if "average_overall_pick_home_draft" in merged and "average_overall_pick_away_draft" in merged:
        merged["draft_pick_diff"] = (
            merged["average_overall_pick_away_draft"] - merged["average_overall_pick_home_draft"]
        )
        features.append("draft_pick_diff")

    X = merged[features].fillna(0)
    y = merged["winner_binary"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # ===================== 6️⃣ EVALUATION =====================
    accuracy = accuracy_score(y_test, y_pred)
    print("\nModel Accuracy:", round(accuracy * 100, 2), "%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Feature importance
    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Coefficient": model.coef_[0]
    }).sort_values("Coefficient", ascending=False)

    print("\nTop Predictive Features:\n", importance_df.head(10))

    # Optional: view data in pandasgui
    # show(merged)

    return model, importance_df, merged


if __name__ == "__main__":
    build_nba_prediction_model()

