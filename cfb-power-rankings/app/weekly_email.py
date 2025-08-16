# Assemble and send the Monday email
import pandas as pd
from datetime import datetime
from .config import TIMEZONE
from .email_utils import send_email

def build_email_html(summary: dict) -> str:
    # Simple HTML with key sections
    parts = [f"<h2>CFB Weekly Report - {datetime.now().strftime('%Y-%m-%d')}</h2>"]
    for title, df in summary.items():
        parts.append(f"<h3>{title}</h3>")
        if isinstance(df, pd.DataFrame):
            parts.append(df.to_html(index=False))
        else:
            parts.append(f"<p>{df}</p>")
    return "\n".join(parts)

def main():
    # Placeholder: Your app will generate CSVs; here we just send a stub message.
    summary = {
        "Status": "Automated email placeholder. Connect to app data exports for full content."
    }
    html = build_email_html(summary)
    send_email("CFB Weekly Report", html, attachments=[])

if __name__ == "__main__":
    main()
