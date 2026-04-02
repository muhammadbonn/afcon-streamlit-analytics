# 🌍 African Football Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://afcon-app-analytics.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458.svg)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Data_Visualization-3F4F75.svg)](https://plotly.com/)

An interactive data visualization dashboard providing deep insights into the historical performance, rankings, and head-to-head records of African national football teams from 1957 to 2026.

**[🔴 View Live Dashboard Here](https://afcon-app-analytics.streamlit.app/)**

## ✨ Key Features
* **Global Filtering:** Toggle instantly between *All African Competitions* and strictly *African Cup of Nations (AFCON)* matches.
* **Historical Rankings:** Analyze top-performing nations over a custom time period or zoom into a specific year.
* **Team Evolution:** Track a specific nation's performance metrics and ranking trajectory over time.
* **Head-to-Head (H2H):** Compare historical match records (Wins, Draws, Losses) between any team and specific opponents, or against all-time top 10/20 teams.
* **Interactive Visualizations:** Powered by Plotly for dynamic, responsive charts.

---
🛠️ Tech Stack

    Framework: Streamlit

    Data Manipulation: Pandas, NumPy

    Data Visualization: Plotly Express

---
## Run Locally
**1. Clone the repository:**

```
git clone [https://github.com/muhammadbonn/afcon-streamlit-analytics.git](https://github.com/muhammadbonn/afcon-streamlit-analytics.git)
cd YOUR_REPO_NAME
```

**2. Install dependencies:**

```
pip install -r requirements.txt
```

**3. Run the Streamlit app:**

```
streamlit run scripts/stream.py
```

---
## 🏗️ Project Architecture
The project follows a clean, modular architecture (Separation of Concerns) to ensure maintainability and fast execution using Streamlit caching.

```text
afcon-streamlit/
├── data/                               # Processed datasets
│   └── african_results_with_stages.csv 
├── scripts/
│   ├── stream.py                       # Main Streamlit application entry point
│   └── utils/                          # Modularized helper functions
│       ├── metrics.py                  # Core statistical and ranking logic
│       ├── charts.py                   # Plotly visualization components
│       ├── ui_helpers.py               # Reusable UI widgets
│       └── tournament.py               # Data staging and extraction
└── requirements.txt                    # Project dependencies
