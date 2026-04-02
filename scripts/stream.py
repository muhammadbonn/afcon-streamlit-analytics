import os
import pandas as pd
import streamlit as st

# Importing core logic and metrics
from utils.tournament import appearances
from utils.metrics import ranking, hth

# Importing chart functions
from utils.charts import plot_top_teams_period, plot_top_teams_year, plot_h2h

# Importing separated views and UI helpers
from utils.views import render_team_investigation_view
from utils.ui_helpers import get_time_selection_ui

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
# Caching & Data Loading Engine
# -------------------------------------------------
@st.cache_data
def load_and_prepare_data(tournament_scope):
    """
    Loads and caches data to dramatically improve dashboard performance.
    Reloads only when the tournament filter changes.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, '../data/african_results_with_stages.csv')
    raw_data = pd.read_csv(path)

    # Apply global filtering based on sidebar selection
    if tournament_scope == 'African Cup of Nations':
        filtered_data = raw_data[raw_data['tournament'] == 'African Cup of Nations'].copy()
    else:
        filtered_data = raw_data.copy()

    # Generate core aggregated dataframes
    app_df = appearances(filtered_data)
    all_time_df = ranking(app_df)

    # Extract dynamic lists for dropdown menus
    teams_list = sorted(all_time_df['team'].unique().tolist())
    top10_list = all_time_df.head(10)['team'].tolist()
    top20_list = all_time_df.head(20)['team'].tolist()

    return filtered_data, app_df, teams_list, top10_list, top20_list

# -------------------------------------------------
# Global Settings (Sidebar)
# -------------------------------------------------
st.sidebar.header("⚙️ Global Settings")
tournament_scope = st.sidebar.selectbox(
    "Select Tournament Scope:",
    ['All Competitions', 'African Cup of Nations']
)

# Fetching data using our cached function
data, appearances_df, all_teams, top10_teams, top20_teams = load_and_prepare_data(tournament_scope)

# -------------------------------------------------
# Sidebar Main Menu
# -------------------------------------------------
st.sidebar.markdown("---") 
first_view_option = st.sidebar.selectbox(
    "What Do You Want to See:",
    ['Investigate Specific Team', 'Ranking Teams', 'Head-to-Head']
)

# =================================================
# 1. Ranking Teams View
# =================================================
if first_view_option == 'Ranking Teams':
    
    # Using our custom reusable UI helper!
    time_type, start_val, end_val = get_time_selection_ui(key_prefix="rank_view")
    
    if time_type == 'period':
        st.subheader("🌍 Ranking Over Specific Period")
        
        result_df = ranking(appearances_df, start=start_val, end=end_val)
        fig = plot_top_teams_period(result_df, start_val, end_val)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📊 View Raw Data (All Teams)"):
            st.dataframe(result_df)

    elif time_type == 'year':
        st.subheader("📅 Ranking in Specific Year")
        
        result_df = ranking(df=appearances_df, year=start_val)
        
        if not result_df.empty:
            fig = plot_top_teams_year(result_df, start_val)
            st.plotly_chart(fig, use_container_width=True)
            with st.expander("📊 View Raw Data"):
                st.dataframe(result_df)
        else:
            st.warning("No matches found for this year.")

# =================================================
# 2. Investigate Specific Team View 
# =================================================
elif first_view_option == 'Investigate Specific Team':
    # Using the separated view module
    render_team_investigation_view(appearances_df, all_teams)

# =================================================
# 3. Head-to-Head View
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
                team=selected_team, matches_data=data, 
                appearances_data=appearances_df, vs=selected_opponents
            )
            
            if not h2h_data.empty:
                fig = plot_h2h(h2h_data, selected_team)
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("📊 View Detailed Head-to-Head Records"):
                    st.dataframe(h2h_data)
            else:
                st.info("No match history found between the selected teams.")
