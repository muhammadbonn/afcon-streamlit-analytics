import pandas as pd
from utils.assumptions import (
    GD_factor, win_factor, draw_factor, 
)
from utils.assumptions import (
    stages_2019_2027, stages_1992_2019, stages_1978_1992,
    stages_1968_1978, stages_1963_1968, stages_1976
)

# A function that defines the tournament system + applies the elimination disorder
def apply_afcon_knockout(df, year, year_idx):
    if year >= 2019:
        stages = stages_2019_2027
    elif year >= 1992:
        stages = stages_1992_2019
    elif year >= 1978:
        stages = stages_1978_1992
    elif year >= 1968:
        stages = stages_1968_1978        
    elif year >= 1963:
        stages = stages_1963_1968
    elif year == 1976:
        stages = stages_1976          
    else:
        return year_idx

    needed = sum(c for _, c in stages)
    if len(year_idx) < needed:
        return year_idx

    ptr = len(year_idx)
    for stage, count in stages:
        df.loc[year_idx[ptr - count:ptr], "stage"] = stage
        ptr -= count

    return year_idx[:ptr]

# Defining the stage of every match using apply_afcon_knockout function
def staging(data):
    df = data.copy()

    # Ensure stage column exists
    if "stage" not in df.columns:
        df["stage"] = pd.NA

    # AFCON only
    mask = df["tournament"] == "African Cup of Nations"

    # Process each tournament year separately
    for year, idx in (
        df[mask]
        .sort_values("date")
        .groupby("year")
        .groups.items()
    ):
        year_idx = list(idx)

        # 1976 AFCON had NO knockout stages (final group system)
        if year == 1976:
            df.loc[year_idx, "stage"] = df.loc[year_idx, "stage"].fillna("Group Stage")
            continue

        # Apply knockout logic
        group_matches = apply_afcon_knockout(df, year, year_idx)

        # Remaining matches are group stage
        df.loc[group_matches, "stage"] = (
            df.loc[group_matches, "stage"]
            .fillna("Group Stage")
        )

    return df

# ------------------------------------------------------------------------------------
# Teams performance in every appearance
def appearances (data):
    # Calculating goals for, goals against, and goals difference for every team's game
    home_df = data.assign(
        team=data["home_team"],
        goals_for=data["home_score"],
        goals_against=data["away_score"])

    away_df = data.assign(
        team=data["away_team"],
        goals_for=data["away_score"],
        goals_against=data["home_score"])

    df = pd.concat([home_df, away_df], ignore_index=True)
    df["goal_difference"] = (df["goals_for"] - df["goals_against"])

    # Result of game: Win, Draw, or Loss
    df["win"] = (df["goals_for"] > df["goals_against"]).astype(int)
    df["draw"] = (df["goals_for"] == df["goals_against"]).astype(int)
    df["loss"] = (df["goals_for"] < df["goals_against"]).astype(int)

    # Derives a weighted performance score combining match outcome, importance, and goal dominance
    df["weighted_match_result"] = (df["win"] * win_factor + df["draw"] * draw_factor) * df["match_value"]
    df["weighted_goal_difference"] = df["goal_difference"].clip(lower=0) * GD_factor
    df["total_points"] = df["weighted_match_result"] + df["weighted_goal_difference"]

    imp_cols = ["team", "goals_for", "goals_against", "goal_difference", "win", "draw", "loss", "total_points", "year"]
    appearances = df[imp_cols].copy()

    return appearances