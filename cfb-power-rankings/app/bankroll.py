# Bankroll accounting with true odds
import pandas as pd

def american_odds_profit(odds: float, stake: float=100.0) -> float:
    if odds is None:
        return 0.0
    if odds > 0:
        return stake * (odds / 100.0)
    else:
        return stake * (100.0 / abs(odds))

def settle_bet(row, stake: float=100.0):
    # row: must include columns ['ats_win','price']
    if row.get("ats_win", False):
        return american_odds_profit(row.get("price", -110), stake)
    return -stake

def bankroll_progress(results_df: pd.DataFrame, starting_bankroll: float=1000.0, stake: float=100.0):
    # results_df should include chronological bets with 'ats_win' and 'price'
    bal = starting_bankroll
    bals = []
    for _, r in results_df.iterrows():
        delta = settle_bet(r, stake)
        bal += delta
        bals.append(bal)
    out = results_df.copy()
    out["bankroll"] = bals
    return out, bal
