# Post-game accuracy report (model & Vegas vs actual)
import pandas as pd
import requests
from datetime import datetime
from .config import CFB_API_KEY
from .rankings import compute_power_scores, fetch_season_stats

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
        rows.append({
            "home_team": g.get("home_team"),
            "away_team": g.get("away_team"),
            "home_points": g.get("home_points"),
            "away_points": g.get("away_points"),
            "week": g.get("week"),
            "start_date": g.get("start_date")
        })
    return pd.DataFrame(rows)

def build_postgame_report(year: int, week: int, model_spreads: pd.DataFrame, vegas_df: pd.DataFrame):
    # model_spreads: columns [home_team, away_team, model_spread_for_home]
    # vegas_df: odds DataFrame with spread 'point' for each team; we'll compute a consensus home spread
    # Compute consensus vegas home spread
    if vegas_df is not None and not vegas_df.empty:
        # Convert to home-centric lines: price/point rows where name matches home/away
        v = vegas_df.copy()
        # For simplicity: average across books, compute home spread as:
        # home_line = average( +point if home listed, -point if away listed )
        # This is a simplification for demonstration.
        def home_spread(grp):
            pts = []
            for _, r in grp.iterrows():
                if r["name"] == r["home_team"]:
                    pts.append(r["point"] or 0.0)
                elif r["name"] == r["away_team"]:
                    pts.append(-(r["point"] or 0.0))
            return sum(pts)/len(pts) if pts else None
        vegas_home = v.groupby(["home_team","away_team","commence_time"]).apply(home_spread).reset_index(name="vegas_home_spread")
    else:
        vegas_home = pd.DataFrame(columns=["home_team","away_team","commence_time","vegas_home_spread"])

    finals = fetch_final_scores(year, week)
    if finals.empty:
        return pd.DataFrame()

    # Actual margin (home - away)
    finals["actual_margin"] = finals["home_points"] - finals["away_points"]

    df = finals.merge(model_spreads, on=["home_team","away_team"], how="left")
    df = df.merge(vegas_home.drop(columns=["commence_time"]), on=["home_team","away_team"], how="left")

    # Errors
    df["model_error_pts"] = (df["model_spread_for_home"] - df["actual_margin"]).abs()
    df["vegas_error_pts"] = (df["vegas_home_spread"] - df["actual_margin"]).abs()

    # Hit/Miss per ATS: sign(model pick) == sign(actual margin minus line)
    df["model_pick_side"] = df["model_spread_for_home"].apply(lambda x: "HOME" if x>=0 else "AWAY")
    df["ats_result_for_model"] = df.apply(lambda r: "WIN" if (r["actual_margin"] - (r["vegas_home_spread"] or 0)) * (1 if r["model_spread_for_home"]>=0 else -1) > 0 else "LOSS", axis=1)

    return df
