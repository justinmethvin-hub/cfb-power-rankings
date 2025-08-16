import pandas as pd
import requests
from app.config import CFB_API_KEY

HEADERS = {"Authorization": f"Bearer {CFB_API_KEY}"} if CFB_API_KEY else {}

def fetch_final_scores(year: int, week: int):
    r = requests.get("https://api.collegefootballdata.com/games",
                     params={"year": year, "week": week, "seasonType": "regular"},
                     headers=HEADERS)
    data = r.json()
    rows = []
    for g in data:
        if g.get("home_points") is None or g.get("away_points") is None:
            continue
        rows.append({"home_team": g.get("home_team"), "away_team": g.get("away_team"),
                     "home_points": g.get("home_points"), "away_points": g.get("away_points"),
                     "week": g.get("week"), "start_date": g.get("start_date")})
    return pd.DataFrame(rows)
