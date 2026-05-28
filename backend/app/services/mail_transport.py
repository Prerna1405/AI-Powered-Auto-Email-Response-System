from sqlalchemy.orm import Session

from app.models.entities import AutoReply, Email, SystemConfig
from app.services.gmail_service import send_via_gmail


def send_reply(db: Session, email: Email, html_reply: str, model_used: str, tokens_used: int = 0):
    cfg = db.query(SystemConfig).first()
    transport = "gmail" if cfg and cfg.gmail_connected else "simulator"
    delivery_status = "sent"
    if transport == "gmail":
        sent = send_via_gmail(email.from_email, email.subject, html_reply)
        delivery_status = "sent" if sent.get("sent") else "failed"

    reply = AutoReply(
        email_id=email.id,
        kb_id=None,
        generated_reply=html_reply,
        ai_confidence=(email.ai_analysis or {}).get("confidence", 0),
        match_method="pipeline",
        delivery_status=delivery_status,
        model_used=model_used,
        tokens_used=tokens_used,
    )
    db.add(reply)
    return transport, reply
