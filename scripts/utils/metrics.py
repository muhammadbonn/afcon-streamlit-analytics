import pandas as pd

# -----------------------------------------------------------------------------------------
# Aggregating teams performance metrics
# -----------------------------------------------------------------------------------------
def ranking(df                                  # Appearances dataframe
            , start = 1957                      # Start year 
            , end = 2026                        # End year
            , year = None                       # Specific year only
            , criteria = "total_points"         # Ranking criteria
           ):

    # Filter data based on the provided time frame
    if year is None:
        data = df[df["year"].between(start, end)]
    else:
        data = df[df["year"] == year]
    
    # Aggregate stats per team
    ranking_data = (data.groupby("team").agg(
        matches = ("team", "count"),
        wins = ("win", "sum"),
        draws = ("draw", "sum"),
        losses = ("loss", "sum"),
        GF = ("goals_for", "sum"),
        GA = ("goals_against", "sum"),
        GD = ("goal_difference", "sum"),
        total_points= ("total_points", "sum"))
    .reset_index())

    # Calculate percentages and final points
    ranking_data["win_%"] = ((ranking_data["wins"] / ranking_data["matches"]) * 100).round(0).astype(int)
    ranking_data["total_points"] = (ranking_data["total_points"] * 100).round(0).astype(int) 
    
    # Sort and establish the rank index
    ranking_data = (
        ranking_data.sort_values(by=criteria, ascending=False)
        .set_index(pd.Index(range(1, len(ranking_data) + 1), name='Rank'))
        )
    
    # Retain 'Rank' as a distinct column for easier accessibility in the H2H function
    ranking_data['Rank'] = ranking_data.index 

    return ranking_data

# -----------------------------------------------------------------------------------------
# Head-to-Head function
# -----------------------------------------------------------------------------------------
def hth(team                   # Required team data
        , matches_data         # Dataframe containing all matches
        , appearances_data     # Dataframe containing team appearances
        , vs = None            # Against the desired team or top teams
        , start = 1957         # Start year 
        , end = 2026           # End year
        , year = None          # Required year to filter 
       ):
    
    hth_columns = ['year', 'home_team', 'away_team', 'home_score', 'away_score']

    # Step 1: Filter DataFrames based on the specified timeframe
    if year is None:
        hth_df = matches_data[matches_data["year"].between(start, end)]
        ranking_data = ranking(appearances_data, start = start, end = end)
    else:
        hth_df = matches_data[matches_data["year"] == year]
        ranking_data = ranking(appearances_data, year = year)

    hth_df = hth_df[hth_columns].copy()
    
    # Step 2: Determine opponent teams list (specific, top teams, or all)
    if vs is not None:
        if isinstance(vs, int):
            teams_list = ranking_data.head(vs)["team"].tolist()
        elif isinstance(vs, list):
            teams_list = vs 
        else:
            teams_list = [vs]
    else:
        teams_list = ranking_data["team"].tolist()
    
    records = []

    # Step 3: Loop through each opponent to compute Head-to-Head stats
    for opponent in teams_list:
        if opponent != team:  # Skip self-match comparisons
            
            # Filter the dataframe for matches strictly between the two teams
            df = hth_df[((hth_df["home_team"] == team) & (hth_df["away_team"] == opponent)) |
                        ((hth_df["away_team"] == team) & (hth_df["home_team"] == opponent))]

            matches_played = len(df)
            
            # Execute calculations only if a match history exists to keep the output clean
            if matches_played > 0:
                wins = sum(
                    ((df["home_team"] == team) & (df["home_score"] > df["away_score"])) |
                    ((df["away_team"] == team) & (df["away_score"] > df["home_score"])))
                draws = sum(df["home_score"] == df["away_score"])
                losses = matches_played - wins - draws
                
                goals_for = sum(df.apply(lambda row: row["home_score"] if row["home_team"] == team else row["away_score"], axis=1))
                goals_against = sum(df.apply(lambda row: row["away_score"] if row["home_team"] == team else row["home_score"], axis=1))
                
                # Use try-except block in case the opponent lacks a recorded rank to prevent KeyError
                try:
                    opp_rank = ranking_data.loc[ranking_data["team"] == opponent, "Rank"].values[0]
                except IndexError:
                    opp_rank = "N/A"

                records.append({
                    "team": team,
                    "opponent": opponent,
                    "opponent_rank": opp_rank, 
                    "matches_played": matches_played,
                    "wins": wins,
                    "draws": draws,
                    "losses": losses,
                    "goals_for": goals_for,
                    "goals_against": goals_against
                })
    
    # Prevent Streamlit rendering errors by returning an empty dataframe with identical columns if no records are found
    if not records:
        return pd.DataFrame(columns=["team", "opponent", "opponent_rank", "matches_played", "wins", "draws", "losses", "goals_for", "goals_against"])
        
    # Aggregate and sort the final DataFrame
    aggregated_df = pd.DataFrame(records).sort_values(by=['matches_played'], ascending=False).reset_index(drop=True)
    return aggregated_df