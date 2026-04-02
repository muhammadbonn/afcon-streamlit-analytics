from utils.extraction import getting_african_data
from utils.tournament import staging
from utils.assumptions import (
    GD_factor, win_factor, draw_factor, 
    tournament_weight, stage_weight
)

# Geting subset of large data for only african temas
path = '../data/all_results.csv'
african_results = getting_african_data(path)

# Defining the knock out and stages of matches
african_with_stages = staging(african_results)
cols = ['year', 'date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'stage']
data = african_with_stages[cols].copy()

# Calculating every match value based on the Weight of the tournament and the stage
data["tournament_weight"] = data["tournament"].map(tournament_weight)
data["stage_weight"] = data["stage"].map(stage_weight).fillna(1.0)
data["match_value"] = (data["tournament_weight"] * data["stage_weight"])

data.to_csv('../data/african_results_with_stages.csv', index=False)
