import pandas as pd

def getting_african_data(path):
    # International football results (1872 to 2026)
    df = pd.read_csv(path)

    # African Cup of Nations from International football results (1872 to 2026)
    afcon = df[df['tournament'] == 'African Cup of Nations']

    # African Cup of Nations qualification from International football results (1872 to 2026)
    afconq = df[df['tournament'] == 'African Cup of Nations qualification']

    # Naming all African teams
    all_african_teams = pd.concat([
        afcon["home_team"], afcon["away_team"],
        afconq["home_team"], afconq["away_team"],])
    african_teams = all_african_teams

    # FIFA World Cup qualification from International football results (1872 to 2026)
    fwcq = df[df['tournament'] == 'FIFA World Cup qualification'].drop_duplicates().reset_index(drop=True)

    # Selecting only FIFA World Cup qualification matches from Africa
    afwcq = fwcq[
        (fwcq["home_team"].isin(african_teams)) &
        (fwcq["away_team"].isin(african_teams))]

    # Merging afcon, afconq, and afwcq to get African teams' games from the three tournaments
    africa = pd.concat([afcon, afconq, afwcq])
    africa["date"] = pd.to_datetime(africa["date"])
    africa["year"] = africa["date"].dt.year

    return africa