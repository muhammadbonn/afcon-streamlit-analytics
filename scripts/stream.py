import os
import pandas as pd
import numpy as np
import streamlit as st

from utils.tournament import appearances
from utils.metrics import ranking, hth
# Importing our new chart functions
from utils.charts import plot_top_teams_period, plot_top_teams_year, plot_team_evolution, plot_h2h

# -------------------------------------------------
# Page Configuration & Description
# -------------------------------------------------
st.set_page_config(
    page_title="African Football Analytics", 
    page_icon="🌍", 
    layout="wide"
)

st.title("🌍 African Football Analytics & Insights")
st.markdown("### Unveiling the Legacy of African Nations")
st.info("**Context & Scope:** This interactive dashboard provides a comprehensive analysis of historical match data, " \
"performance metrics, and all-time rankings for African national teams across major tournaments.")

# -------------------------------------------------
# Reading & Preparing Data
# -------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, '../data/african_results_with_stages.csv')
data = pd.read_csv(path)

# Creating Dataframes
appearances_df = appearances(data)
all_time = ranking(appearances_df)

# Extracting basic lists for dropdowns
all_teams = sorted(all_time['team'].unique().tolist())
top10_teams = all_time.head(10)['team'].tolist()
top20_teams = all_time.head(20)['team'].tolist()

# -------------------------------------------------
# Sidebar Main Menu
# -------------------------------------------------
first_view_option = st.sidebar.selectbox(
    "What Do You Want to See:",
    ['Investigate Specific Team', 'Ranking Teams', 'Head-to-Head']
)

# =================================================
# 1. Ranking Teams
# =================================================
if first_view_option == 'Ranking Teams':
    time_option = st.sidebar.selectbox(
        "What Years are You Intersted in:",
        ['Ranking Over Specific Period', 'Ranking in Specific Year']
    )
    
    if time_option == 'Ranking Over Specific Period':
        st.subheader("🌍 Ranking Over Specific Period")
        
        start_year, end_year = st.sidebar.slider(
            "Select Period:",
            min_value=1957, max_value=2026, value=(1957, 2026)
        )
        
        result_df = ranking(appearances_df, start=start_year, end=end_year)
        
        # Calling the chart function from utils
        fig = plot_top_teams_period(result_df, start_year, end_year)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📊 View Raw Data (All Teams)"):
            st.dataframe(result_df)

    elif time_option == 'Ranking in Specific Year':
        st.subheader("📅 Ranking in Specific Year")
        
        years_list = list(range(1957, 2027))
        specific_year = st.sidebar.selectbox(
            "Select Year:", years_list, index=len(years_list) - 1
        )
        
        result_df = ranking(df=appearances_df, year=specific_year)
        
        if not result_df.empty:
            # Calling the chart function from utils
            fig = plot_top_teams_year(result_df, specific_year)
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📊 View Raw Data"):
                st.dataframe(result_df)
        else:
            st.warning("No matches found for this year.")

# =================================================
# 2. Investigate Specific Team
# =================================================
elif first_view_option == 'Investigate Specific Team':
    selected_team = st.sidebar.selectbox(
        "Select Desired Team:",
        all_teams, index=None, placeholder="Type or select a team..."
    )
    
    if selected_team:
        st.success(f"Investigating: {selected_team}")
        
        time_option = st.sidebar.selectbox(
            "What Years are You Intersted in:",
            ['Ranking Over Specific Period', 'Ranking in Specific Year']
        )
        
        if time_option == 'Ranking Over Specific Period':
            st.subheader(f"📈 {selected_team} Evolution Over Period")
            
            start_year, end_year = st.sidebar.slider(
                "Select Period:", min_value=1957, max_value=2026, value=(1957, 2026)
            )

            years_to_investigate = range(start_year, end_year + 1) 
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
                
                # Calling the chart function from utils
                fig = plot_team_evolution(evolution_df, selected_team, start_year, end_year)
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("📊 View Yearly Breakdown Data"):
                    st.dataframe(evolution_df[['year', 'Rank', 'matches', 'wins', 'draws', 'losses', 'total_points', 'win_%']])
            else:
                st.warning(f"No matches found for {selected_team} in this period.")

        elif time_option == 'Ranking in Specific Year':
            st.subheader(f"🎯 {selected_team} Performance in {specific_year if 'specific_year' in locals() else 'Selected Year'}")
            
            years_list = list(range(1957, 2027))
            specific_year = st.sidebar.selectbox(
                "Select Year:", years_list, index=len(years_list) - 1
            )
            
            yearly_rank = ranking(appearances_df, year=specific_year)
            team_data = yearly_rank[yearly_rank['team'] == selected_team]
            
            if not team_data.empty:
                st.markdown(f"### Rank: #{team_data['Rank'].values[0]}")
                
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
                st.warning(f"{selected_team} did not play any matches in {specific_year}.")

# =================================================
# 3. Head-to-Head
# =================================================
elif first_view_option == 'Head-to-Head':
    selected_team = st.sidebar.selectbox(
        "Select Desired Team:",
        all_teams, index=None, placeholder="Type or select a team..."
    )
    
    if selected_team:
        opponent_type = st.sidebar.selectbox(
            "What are the Opponent Teams:",
            ['Top 10 Teams (All Time)', 'Top 20 Teams (All Time)', 'Specific Team/Teams']
        )
        
        selected_opponents = []
        if opponent_type == 'Specific Team/Teams':
            selected_opponents = st.sidebar.multiselect(
                "Select Opponent Team/Teams:",
                all_teams, placeholder="Choose one or more teams..." 
            )
        elif opponent_type == 'Top 10 Teams (All Time)':
            selected_opponents = top10_teams
        elif opponent_type == 'Top 20 Teams (All Time)':
            selected_opponents = top20_teams

        if selected_opponents:
            st.subheader(f"⚔️ {selected_team} vs Opponents")
            
            h2h_data = hth(
                team=selected_team, 
                matches_data=data, 
                appearances_data=appearances_df, 
                vs=selected_opponents
            )
            
            if not h2h_data.empty:
                # Calling the chart function from utils
                fig = plot_h2h(h2h_data, selected_team)
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("📊 View Detailed Head-to-Head Records"):
                    st.dataframe(h2h_data)
            else:
                st.info("No match history found between the selected teams.")
