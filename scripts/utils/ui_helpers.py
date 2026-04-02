import streamlit as st

# -----------------------------------------------------------------------------------------
# Reusable UI Component: Time Selection
# -----------------------------------------------------------------------------------------
def get_time_selection_ui(key_prefix="default"):
    """
    Renders the time selection UI in the sidebar and returns the user's choice.
    Returns a tuple: (time_type, start_val, end_val)
    """
    time_option = st.sidebar.selectbox(
        "What Years are You Interested in:",
        ['Ranking Over Specific Period', 'Ranking in Specific Year'],
        key=f"{key_prefix}_time_option" # Using key_prefix prevents Streamlit duplicate errors
    )
    
    if time_option == 'Ranking Over Specific Period':
        start_year, end_year = st.sidebar.slider(
            "Select Period:", 
            min_value=1957, max_value=2026, value=(1957, 2026),
            key=f"{key_prefix}_period_slider"
        )
        return "period", start_year, end_year
    else:
        years_list = list(range(1957, 2027))
        specific_year = st.sidebar.selectbox(
            "Select Year:", 
            years_list, index=len(years_list) - 1,
            key=f"{key_prefix}_year_select"
        )
        return "year", specific_year, None
