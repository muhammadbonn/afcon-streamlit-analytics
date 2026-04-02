import pandas as pd
import numpy as np
import streamlit as st
import os

from utils.tournament import appearances
from utils.metrics import ranking, hth

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
        
        # Slider to select a time range
        start_year, end_year = st.sidebar.slider(
            "Select Period:",
            min_value=1957, max_value=2026, value=(1957, 2026)
        )
        
        result_df = ranking(appearances_df, start=start_year, end=end_year)
        st.dataframe(result_df)

    elif time_option == 'Ranking in Specific Year':
        st.subheader("📅 Ranking in Specific Year")
        
        years_list = list(range(1957, 2027))
        specific_year = st.sidebar.selectbox(
            "Select Year:", years_list, index=len(years_list) - 1
        )
        
        result_df = ranking(df=appearances_df, year=specific_year)
        st.dataframe(result_df)

# =================================================
# 2. Investigate Specific Team
# =================================================
elif first_view_option == 'Investigate Specific Team':
    selected_team = st.sidebar.selectbox(
        "Select Desired Team:",
        all_teams, index=None, placeholder="Type or select a team..."
    )
    
    # Proceed only if a team is selected
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

            # Build Time Evolution DataFrame
            # Added +1 to ensure the end_year is included in the range
            years_to_investigate = range(start_year, end_year + 1) 
            all_years_data = []

            for year in years_to_investigate:
                yearly_rank = ranking(appearances_df, year=year)
                # Filter specifically for the selected team
                team_data = yearly_rank[yearly_rank['team'] == selected_team]
                
                # Check if the team actually played matches in this specific year
                if not team_data.empty: 
                    all_years_data.append(team_data)

            # Display the concatenated dataframe if data exists
            if all_years_data:
                evolution_df = pd.concat(all_years_data, ignore_index=True)
                st.dataframe(evolution_df)
            else:
                st.warning(f"No matches found for {selected_team} in this period.")

        elif time_option == 'Ranking in Specific Year':
            st.subheader(f"🎯 {selected_team} Ranking in Specific Year")
            
            years_list = list(range(1957, 2027))
            specific_year = st.sidebar.selectbox(
                "Select Year:", years_list, index=len(years_list) - 1
            )
            
            # Calculate ranking for the year and isolate the selected team
            yearly_rank = ranking(appearances_df, year=specific_year)
            team_data = yearly_rank[yearly_rank['team'] == selected_team]
            
            if not team_data.empty:
                st.dataframe(team_data)
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
        
        if opponent_type == 'Specific Team/Teams':
            selected_opponents = st.sidebar.multiselect(
                "Select Opponent Team/Teams:",
                all_teams, placeholder="Choose one or more teams..." 
            )
            
            if selected_opponents:
                st.subheader(f"⚔️ {selected_team} vs Selected Opponents")
                # Passed both matches_data and appearances_data to the hth function
                st.dataframe(hth(
                    team=selected_team, 
                    matches_data=data, 
                    appearances_data=appearances_df, 
                    vs=selected_opponents
                ))

        elif opponent_type == 'Top 10 Teams (All Time)':
            st.subheader(f"⚔️ {selected_team} vs Top 10 Teams")
            st.dataframe(hth(
                team=selected_team, 
                matches_data=data, 
                appearances_data=appearances_df, 
                vs=top10_teams
            ))

        elif opponent_type == 'Top 20 Teams (All Time)':
            st.subheader(f"⚔️ {selected_team} vs Top 20 Teams")
            st.dataframe(hth(
                team=selected_team, 
                matches_data=data, 
                appearances_data=appearances_df, 
                vs=top20_teams
            ))
