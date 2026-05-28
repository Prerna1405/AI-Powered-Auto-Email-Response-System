import base64
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from app.core.config import settings


def _client():
    if not all([settings.gmail_client_id, settings.gmail_client_secret, settings.gmail_refresh_token]):
        return None
    creds = Credentials(
        None,
        refresh_token=settings.gmail_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.gmail_client_id,
        client_secret=settings.gmail_client_secret,
        scopes=[
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.modify",
        ],
    )
    return build("gmail", "v1", credentials=creds)


def send_via_gmail(to_email: str, subject: str, html: str):
    client = _client()
    if not client:
        return {"sent": False, "reason": "gmail_not_configured"}
    msg = MIMEText(html, "html")
    msg["to"] = to_email
    msg["subject"] = f"Re: {subject}"
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    client.users().messages().send(userId="me", body={"raw": raw}).execute()
    return {"sent": True}


def fetch_unread(limit: int = 10):
    client = _client()
    if not client:
        return []
    items = client.users().messages().list(userId="me", q="is:unread", maxResults=limit).execute()
    return items.get("messages", [])
