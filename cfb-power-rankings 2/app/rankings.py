import pandas as pd
import numpy as np
import requests
from app.config import CFB_API_KEY

HEADERS = {"Authorization": f"Bearer {CFB_API_KEY}"} if CFB_API_KEY else {}

def zscore(s: pd.Series):
    return (s - s.mean()) / (s.std(ddof=0) if s.std(ddof=0) != 0 else 1)

def fetch_season_stats(year: int):
    params = {"year": year, "seasonType": "regular"}
    off = requests.get("https://api.collegefootballdata.com/stats/season",
                       params={**params, "category": "offense"}, headers=HEADERS).json()
    deff = requests.get("https://api.collegefootballdata.com/stats/season",
                        params={**params, "category": "defense"}, headers=HEADERS).json()

    def to_df(items):
        data = {}
        for it in items:
            team = it.get("team")
            stat = it.get("statName")
            val = it.get("statValue")
            data.setdefault(team, {})[stat] = pd.to_numeric(val, errors="coerce")
        return pd.DataFrame.from_dict(data, orient="index")

    df_off = to_df(off)
    df_def = to_df(deff)

    mapping = {"Yards Per Play": "Off_YPP", "Points Per Play": "Off_PPP"}
    df_off = df_off[[c for c in mapping if c in df_off.columns]].rename(columns=mapping)

    mapping_def = {"Opp Yards Per Play": "Def_YPP", "Opp Points Per Play": "Def_PPP"}
    df_def = df_def[[c for c in mapping_def if c in df_def.columns]].rename(columns=mapping_def)

    df = df_off.join(df_def, how="inner").dropna()
    return df.reset_index().rename(columns={"index": "Team"})

def compute_power_scores(df: pd.DataFrame, weights=None):
    if weights is None:
        weights = {"Off_YPP": 0.25, "Off_PPP": 0.25, "Def_YPP": -0.25, "Def_PPP": -0.25}
    zcols = {}
    for col in weights.keys():
        zcols[col] = zscore(df[col]) if col in df.columns else pd.Series(0, index=df.index)
    zdf = pd.DataFrame(zcols)
    df["Power_Score"] = sum(zdf[c] * w for c, w in weights.items())
    df = df.sort_values("Power_Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df[["Rank", "Team", "Power_Score"] + list(weights.keys())]
