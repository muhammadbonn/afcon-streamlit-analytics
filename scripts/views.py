import pandas as pd
import streamlit as st
from utils.metrics import ranking
from utils.charts import plot_team_evolution
from utils.ui_helpers import get_time_selection_ui

# -----------------------------------------------------------------------------------------
# View Component: Investigate Specific Team
# -----------------------------------------------------------------------------------------
def render_team_investigation_view(appearances_df, all_teams):
    """
    Renders the UI and logic for investigating a specific team's historical performance.
    """
    
    selected_team = st.sidebar.selectbox(
        "Select Desired Team:",
        all_teams, index=None, placeholder="Type or select a team..."
    )
    
    if selected_team:
        st.success(f"Investigating: {selected_team}")
        
        # Calling our reusable UI component!
        time_type, start_val, end_val = get_time_selection_ui(key_prefix="team_view")
        
        # ---------------------------------------------------------
        # Option A: Over a Specific Period
        # ---------------------------------------------------------
        if time_type == 'period':
            st.subheader(f"📈 {selected_team} Evolution Over Period")
            
            # start_val = start_year, end_val = end_year
            years_to_investigate = range(start_val, end_val + 1) 
            all_years_data = []

            for year in years_to_investigate:
                yearly_rank = ranking(appearances_df, year=year)
                team_data = yearly_rank[yearly_rank['team'] == selected_team]
                
                if not team_data.empty: 
                    team_data = team_data.copy()
                    team_data['year'] = year
                    all_years_data.append(team_data)

            if all_years_data:
                evolution_df = pd.concat(all_years_data, ignore_index=True)
                
                fig = plot_team_evolution(evolution_df, selected_team, start_val, end_val)
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("📊 View Yearly Breakdown Data"):
                    st.dataframe(evolution_df[['year', 'Rank', 'matches', 'wins', 'draws', 'losses', 'total_points', 'win_%']])
            else:
                st.warning(f"No matches found for {selected_team} in this period.")

        # ---------------------------------------------------------
        # Option B: In a Specific Year
        # ---------------------------------------------------------
        elif time_type == 'year':
            st.subheader(f"🎯 {selected_team} Performance")
            
            # start_val = specific_year
            yearly_rank = ranking(appearances_df, year=start_val)
            team_data = yearly_rank[yearly_rank['team'] == selected_team]
            
            if not team_data.empty:
                st.markdown(f"### Global Rank: #{team_data['Rank'].values[0]}")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Matches Played", int(team_data['matches'].values[0]))
                col2.metric("Wins", int(team_data['wins'].values[0]))
                col3.metric("Win Rate", f"{int(team_data['win_%'].values[0])}%")
                col4.metric("Total Points", int(team_data['total_points'].values[0]))
                
                col5, col6, col7 = st.columns(3)
                col5.metric("Goals For (GF)", int(team_data['GF'].values[0]))
                col6.metric("Goals Against (GA)", int(team_data['GA'].values[0]))
                col7.metric("Goal Difference (GD)", int(team_data['GD'].values[0]))
            else:
                st.warning(f"{selected_team} did not play any matches in {start_val}.")
