import pandas as pd
from datetime import datetime
from app.email_utils import send_email

def build_email_html(summary: dict) -> str:
    parts = [f"<h2>CFB Weekly Report - {datetime.now().strftime('%Y-%m-%d')}</h2>"]
    for title, df in summary.items():
        parts.append(f"<h3>{title}</h3>")
        if isinstance(df, pd.DataFrame):
            parts.append(df.to_html(index=False))
        else:
            parts.append(f"<p>{df}</p>")
    return "\n".join(parts)

def main():
    summary = {"Status": "Automated email placeholder. Connect to app data exports for full content."}
    html = build_email_html(summary)
    send_email("CFB Weekly Report", html, attachments=[])

if __name__ == "__main__":
    main()
