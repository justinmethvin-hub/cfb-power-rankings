import pandas as pd

def american_odds_profit(odds: float, stake: float=100.0) -> float:
    if odds is None:
        return 0.0
    if odds > 0:
        return stake * (odds / 100.0)
    else:
        return stake * (100.0 / abs(odds))

def settle_bet(row, stake: float=100.0):
    if row.get("ats_win", False):
        return american_odds_profit(row.get("price", -110), stake)
    return -stake

def bankroll_progress(results_df: pd.DataFrame, starting_bankroll: float=1000.0, stake: float=100.0):
    bal = starting_bankroll
    bals = []
    for _, r in results_df.iterrows():
        bal += settle_bet(r, stake)
        bals.append(bal)
    out = results_df.copy()
    out["bankroll"] = bals
    return out, bal
