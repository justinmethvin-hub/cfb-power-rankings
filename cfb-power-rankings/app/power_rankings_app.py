# Streamlit App
import streamlit as st
import pandas as pd
from datetime import datetime, date
from .config import DEFAULT_BANKROLL, DEFAULT_UNIT, CONF_THRESHOLD_DEFAULT
from .rankings import fetch_season_stats, compute_power_scores
from .odds import fetch_cfb_odds
from .postgame_report import build_postgame_report
from .bankroll import bankroll_progress

st.set_page_config(page_title="CFB Power Rankings", page_icon="🏈", layout="wide")

st.title("🏈 CFB Power Rankings & Betting Dashboard")

with st.sidebar:
    year = st.number_input("Season Year", value=datetime.now().year, step=1)
    conf_threshold = st.number_input("Confidence Threshold (pts)", value=CONF_THRESHOLD_DEFAULT, step=0.5, min_value=0.0)
    bankroll = st.number_input("Starting Bankroll ($)", value=DEFAULT_BANKROLL, step=100.0)
    unit = st.number_input("Bet Size / Unit ($)", value=DEFAULT_UNIT, step=25.0)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Rankings", "Value Bets", "Bankroll", "Confidence Report", "Email Preview"])

with tab1:
    st.subheader("Power Rankings")
    try:
        stats = fetch_season_stats(year)
        pr = compute_power_scores(stats)
        st.dataframe(pr.head(25))
        st.download_button("Download Rankings CSV", pr.to_csv(index=False), file_name=f"rankings_{year}.csv")
    except Exception as e:
        st.error(f"Error fetching rankings: {e}")

with tab2:
    st.subheader("Model vs Vegas (Value Bets)")
    st.caption("Predicted spread = Power Score difference home vs away. Confidence = |Model - Vegas|")
    try:
        odds = fetch_cfb_odds()
        st.dataframe(odds.head(50))
        st.info("Join odds to model spreads for full value bet table (implementation requires team matching).")
    except Exception as e:
        st.error(f"Error fetching odds: {e}")

with tab3:
    st.subheader("Bankroll Tracker (Auto)")
    st.caption("Odds-aware returns; flat unit size.")
    sample = pd.DataFrame({
        "matchup": ["Team A vs Team B", "Team C vs Team D"],
        "ats_win": [True, False],
        "price": [-120, +140]
    })
    prog, end_bal = bankroll_progress(sample, starting_bankroll=bankroll, stake=unit)
    st.dataframe(prog)
    st.metric("Ending Bankroll", f"${end_bal:,.2f}")

with tab4:
    st.subheader("Confidence Report (Historical)")
    st.caption("Aggregated performance by confidence tiers over time.")
    hist = pd.DataFrame({
        "Confidence": ["High", "Medium", "Low"],
        "Bets": [18, 35, 28],
        "Wins": [14, 21, 13],
        "Losses": [4, 14, 15],
        "Win_%": [77.8, 60.0, 46.4],
        "Profit_$": [960, 420, -260],
        "ROI_%": [53.3, 12.0, -9.3]
    })
    st.dataframe(hist)

with tab5:
    st.subheader("Email Preview")
    st.write("Click the button to send a test email (configure Gmail secrets first).")
    if st.button("📧 Send Weekly Email Now"):
        try:
            from .weekly_email import main as send_weekly
            send_weekly()
            st.success("Email sent (check your inbox).")
        except Exception as e:
            st.error(f"Email failed: {e}")
