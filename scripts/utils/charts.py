import plotly.express as px

# -----------------------------------------------------------------------------------------
# Plot: Top Teams Over a Period
# -----------------------------------------------------------------------------------------
def plot_top_teams_period(df, start_year, end_year):
    # We take only the top 15 teams to keep the bar chart readable
    fig = px.bar(
        df.head(15), 
        x='team', y='total_points', 
        title=f'Top 15 Teams by Total Points ({start_year} - {end_year})',
        color='total_points', color_continuous_scale='Viridis'
    )
    return fig

# -----------------------------------------------------------------------------------------
# Plot: Top Teams in a Specific Year
# -----------------------------------------------------------------------------------------
def plot_top_teams_year(df, year):
    fig = px.bar(
        df.head(15), 
        x='team', y='total_points', 
        title=f'Top 15 Teams in {year}',
        color='win_%', color_continuous_scale='Blues',
        labels={'win_%': 'Win Rate %'}
    )
    return fig

# -----------------------------------------------------------------------------------------
# Plot: Team Ranking Evolution Over Time
# -----------------------------------------------------------------------------------------
def plot_team_evolution(df, team, start_year, end_year):
    fig = px.line(
        df, 
        x='year', y='Rank', 
        title=f"{team}'s Ranking Evolution ({start_year} - {end_year})",
        markers=True
    )
    # Invert Y-axis because Rank 1 (Top) should be at the top of the chart
    fig.update_yaxes(autorange="reversed")
    return fig

# -----------------------------------------------------------------------------------------
# Plot: Head-to-Head Outcomes
# -----------------------------------------------------------------------------------------
def plot_h2h(df, team):
    fig = px.bar(
        df, 
        x='opponent', 
        y=['wins', 'draws', 'losses'], 
        title=f'Match Outcomes: {team} vs Opponents',
        labels={'value': 'Number of Matches', 'variable': 'Outcome', 'opponent': 'Opponent'},
        barmode='group',
        color_discrete_map={'wins': '#2ca02c', 'draws': '#ff7f0e', 'losses': '#d62728'} # Green, Orange, Red
    )
    return fig
