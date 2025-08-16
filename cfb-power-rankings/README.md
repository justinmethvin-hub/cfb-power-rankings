# College Football Power Rankings (Streamlit + Odds + Email)

A complete CFB betting model with:
- Power rankings from stats (SP+, YPP/PPP, TO margin, Special Teams)
- Model vs. Vegas spread comparison (TheOddsAPI)
- Confidence scoring with emoji tiers
- Post-game accuracy report (model & Vegas vs actual)
- Bankroll tracking with **true odds payouts**
- Monday email summary (rankings, value bets, performance, CSV)
- Deploy-ready for **Streamlit Cloud** + optional GitHub Actions for weekly email

## Quick Start (Streamlit Cloud)
1. Create a new GitHub repo and push this project (or fork the temporary repo).
2. On Streamlit Cloud, deploy `app/power_rankings_app.py`.
3. Add secrets via `.streamlit/secrets.toml` (or Streamlit Cloud Secrets UI).

### `.streamlit/secrets.toml` template
```toml
CFB_API_KEY = "your_collegefootballdata_key"
ODDS_API_KEY = "your_theoddsapi_key"
GMAIL_USER = "your_email@gmail.com"
GMAIL_PASS = "your_16_char_gmail_app_password"
EMAIL_TO = "destination_email@example.com"
TIMEZONE = "America/Chicago"
```

> **Note:** Streamlit Cloud won’t run background jobs by itself. Use the **Email Preview** button in the app to send on-demand. For fully automatic Monday emails, use the included **GitHub Actions** workflow or a Render cron job.

## Local Dev (optional)
```bash
pip install -r requirements.txt
streamlit run app/power_rankings_app.py
```

## Features
- **Confidence Filters:** filter value bets by LOW / MED / HIGH or by numeric threshold
- **Bankroll Tracker:** defaults to $1,000 bankroll and $100 flat units; accounts for real odds payouts
- **Historical Confidence Report:** win%, avg error, ROI per tier over time
- **CSV Exports:** rankings, value bets, and post-game reports

## GitHub Actions (Optional: Monday Email)
- Workflow file: `.github/workflows/monday-email.yml`
- Sets a cron for Monday 09:00 America/Chicago to send the weekly email via `app/weekly_email.py`
- **Set repo secrets** to use Actions:
  - `CFB_API_KEY`, `ODDS_API_KEY`, `GMAIL_USER`, `GMAIL_PASS`, `EMAIL_TO`

## Files
- `app/power_rankings_app.py` — Streamlit dashboard
- `app/rankings.py` — pulls stats & computes power scores
- `app/odds.py` — pulls odds & normalizes lines
- `app/postgame_report.py` — builds post-game accuracy report
- `app/bankroll.py` — bankroll accounting w/ true odds
- `app/email_utils.py` — Gmail SMTP email sender
- `app/weekly_email.py` — assembles and sends Monday report
- `.streamlit/secrets.toml` — secrets template
- `.github/workflows/monday-email.yml` — optional weekly automation
- `requirements.txt` — dependencies

## Security
Keep credentials only in **Secrets**:
- Streamlit Cloud Secrets
- GitHub Repository Secrets
- Replit Secrets (if testing)

---

Made for Justin’s Monday insights 🏈
