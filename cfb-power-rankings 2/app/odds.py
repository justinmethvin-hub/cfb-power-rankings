import pandas as pd
import requests
from app.config import ODDS_API_KEY

def fetch_cfb_odds(markets=("spreads",), regions=("us",), odds_format="american"):
    params = {"apiKey": ODDS_API_KEY, "regions": ",".join(regions), "markets": ",".join(markets), "oddsFormat": odds_format}
    r = requests.get("https://api.the-odds-api.com/v4/sports/americanfootball_ncaaf/odds", params=params)
    data = r.json()
    rows = []
    for game in data:
        home = game.get("home_team"); away = game.get("away_team"); commence = game.get("commence_time")
        for bk in game.get("bookmakers", []):
            for mk in bk.get("markets", []):
                if mk.get("key") == "spreads":
                    for out in mk.get("outcomes", []):
                        rows.append({"home_team": home, "away_team": away, "commence_time": commence,
                                     "bookmaker": bk.get("key"), "name": out.get("name"),
                                     "point": out.get("point"), "price": out.get("price")})
    return pd.DataFrame(rows)
