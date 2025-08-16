import os
import streamlit as st

def get_secret(key: str, default: str = None):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)

CFB_API_KEY = get_secret("CFB_API_KEY", "")
ODDS_API_KEY = get_secret("ODDS_API_KEY", "")
GMAIL_USER = get_secret("GMAIL_USER", "")
GMAIL_PASS = get_secret("GMAIL_PASS", "")
EMAIL_TO = get_secret("EMAIL_TO", GMAIL_USER)
TIMEZONE = get_secret("TIMEZONE", "America/Chicago")
DEFAULT_BANKROLL = 1000.0
DEFAULT_UNIT = 100.0
CONF_THRESHOLD_DEFAULT = 2.0
