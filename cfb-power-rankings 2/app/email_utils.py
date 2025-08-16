import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from app.config import GMAIL_USER, GMAIL_PASS, EMAIL_TO

def send_email(subject: str, html_body: str, attachments=None, to_addr: str = None):
    to_addr = to_addr or EMAIL_TO or GMAIL_USER
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_addr
    msg['Subject'] = subject

    msg.attach(MIMEText(html_body, 'html'))

    for path in (attachments or []):
        part = MIMEBase('application', 'octet-stream')
        with open(path, 'rb') as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(path)}"')
        msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
