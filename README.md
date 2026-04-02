![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)

An interactive data visualization dashboard providing deep insights into the historical performance, rankings, and head-to-head records of African national football teams from 1957 to 2026.

**[View Interactive Dashboard Here](https://afcon-app-analytics.streamlit.app/)**

## Key Features
* **Global Filtering:** Toggle instantly between *All African Competitions* and strictly *African Cup of Nations (AFCON)* matches.
* **Historical Rankings:** Analyze top-performing nations over a custom time period or zoom into a specific year.
* **Team Evolution:** Track a specific nation's performance metrics and ranking trajectory over time.
* **Head-to-Head (H2H):** Compare historical match records (Wins, Draws, Losses) between any team and specific opponents, or against all-time top 10/20 teams.
* **Interactive Visualizations:** Powered by Plotly for dynamic, responsive charts.

---
## Tech Stack

    Framework: Streamlit

    Data Manipulation: Pandas, NumPy

    Data Visualization: Plotly Express

---
## Run Locally
**1. Clone the repository:**

```
git clone https://github.com/muhammadbonn/afcon-streamlit-analytics.git
cd afcon-streamlit-analytics
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
## Project Architecture
The project follows a clean, modular architecture (Separation of Concerns) to ensure maintainability and fast execution using Streamlit caching.

```text
afcon-streamlit-analytics/
├── data/                                     
│   ├── all_results.csv                       # Raw dataset
│   └── african_results_with_stages.csv       # Processed dataset
├── scripts/
│   ├── getting_african_data.py               # Processing and saving African data
│   ├── stream.py                             # Main Streamlit application entry point
│   └── utils/                                # Modularized helper functions
├── requirements.txt                          # Project dependencies
└── README.md
