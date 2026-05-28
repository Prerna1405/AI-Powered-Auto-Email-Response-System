from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import AutoReply, Email, KnowledgeBase, SystemConfig
from app.schemas.common import EmailCreate, EmailOut, KBCreate, KBOut, SettingsUpdate
from app.services.gmail_service import fetch_unread
from app.services.pipeline import process_email
from app.workers.tasks import process_email_task

router = APIRouter(prefix="/api")


@router.post("/emails/simulate-send")
def simulate_send(payload: EmailCreate, db: Session = Depends(get_db)):
    email = Email(**payload.model_dump(), status="unprocessed")
    db.add(email)
    db.commit()
    db.refresh(email)
    process_email_task.delay(email.id)
    return {"id": email.id, "status": "queued"}


@router.get("/emails", response_model=list[EmailOut])
def list_emails(folder: str = Query("all"), db: Session = Depends(get_db)):
    q = db.query(Email)
    if folder == "inbox":
        q = q.filter(Email.status.in_(["unprocessed", "processing"]))
    elif folder == "sent":
        q = q.filter(Email.status == "replied")
    elif folder == "escalated":
        q = q.filter(Email.status == "escalated")
    elif folder == "failed":
        q = q.filter(Email.status == "failed")
    return q.order_by(Email.received_at.desc()).all()


@router.get("/emails/{email_id}")
def get_email(email_id: str, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    reply = db.query(AutoReply).filter(AutoReply.email_id == email.id).first()
    return {"email": email, "reply": reply}


@router.post("/emails/{email_id}/process")
def process_email_manual(email_id: str, db: Session = Depends(get_db)):
    process_email_task.delay(email_id)
    return {"ok": True, "status": "queued"}


@router.post("/emails/{email_id}/send-reply")
def resend_reply(email_id: str, db: Session = Depends(get_db)):
    process_email_task.delay(email_id)
    return {"ok": True, "status": "queued"}


@router.get("/kb", response_model=list[KBOut])
def list_kb(db: Session = Depends(get_db)):
    return db.query(KnowledgeBase).all()


@router.post("/kb", response_model=KBOut)
def create_kb(payload: KBCreate, db: Session = Depends(get_db)):
    kb = KnowledgeBase(**payload.model_dump())
    db.add(kb)
    db.commit()
    db.refresh(kb)
    return kb


@router.put("/kb/{kb_id}", response_model=KBOut)
def update_kb(kb_id: str, payload: KBCreate, db: Session = Depends(get_db)):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="KB not found")
    for k, v in payload.model_dump().items():
        setattr(kb, k, v)
    db.commit()
    db.refresh(kb)
    return kb


@router.delete("/kb/{kb_id}")
def delete_kb(kb_id: str, db: Session = Depends(get_db)):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="KB not found")
    db.delete(kb)
    db.commit()
    return {"deleted": True}


@router.post("/kb/test")
def test_kb(payload: EmailCreate, db: Session = Depends(get_db)):
    email = Email(**payload.model_dump(), status="unprocessed")
    db.add(email)
    db.commit()
    db.refresh(email)
    process_email_task.delay(email.id)
    return {"ok": True, "status": "queued", "email_id": email.id}


@router.get("/analytics/overview")
def analytics_overview(db: Session = Depends(get_db)):
    total = db.query(Email).count()
    replied = db.query(Email).filter(Email.status == "replied").count()
    escalated = db.query(Email).filter(Email.status == "escalated").count()
    failed = db.query(Email).filter(Email.status == "failed").count()
    return {
        "total": total,
        "auto_resolved_pct": (replied / total * 100) if total else 0,
        "escalated_pct": (escalated / total * 100) if total else 0,
        "failed": failed,
    }


@router.get("/analytics/categories")
def analytics_categories(db: Session = Depends(get_db)):
    emails = db.query(Email).all()
    counts = {}
    for item in emails:
        category = (item.ai_analysis or {}).get("category", "Unknown")
        counts[category] = counts.get(category, 0) + 1
    return counts


@router.get("/analytics/kb-coverage")
def kb_coverage(db: Session = Depends(get_db)):
    intents = {kb.intent for kb in db.query(KnowledgeBase).all()}
    analyzed = [e for e in db.query(Email).all() if e.ai_analysis]
    covered = sum(1 for e in analyzed if e.ai_analysis.get("intent") in intents)
    return {"coverage_pct": (covered / len(analyzed) * 100) if analyzed else 0}


@router.post("/gmail/connect")
def gmail_connect(db: Session = Depends(get_db)):
    cfg = db.query(SystemConfig).first()
    if not cfg:
        cfg = SystemConfig()
        db.add(cfg)
    cfg.gmail_connected = True
    db.commit()
    return {"connected": True, "mode": "gmail"}


@router.get("/gmail/status")
def gmail_status(db: Session = Depends(get_db)):
    cfg = db.query(SystemConfig).first()
    return {"connected": bool(cfg and cfg.gmail_connected)}


@router.post("/gmail/disconnect")
def gmail_disconnect(db: Session = Depends(get_db)):
    cfg = db.query(SystemConfig).first()
    if cfg:
        cfg.gmail_connected = False
        db.commit()
    return {"connected": False}


@router.post("/gmail/sync")
def gmail_sync(db: Session = Depends(get_db)):
    messages = fetch_unread(limit=25)
    for msg in messages:
        email = Email(
            message_id=msg.get("id"),
            from_email="gmail-user@example.com",
            from_name="Gmail User",
            subject="Synced from Gmail",
            body="Fetched unread email body placeholder.",
            status="unprocessed",
            transport_mode="gmail",
        )
        db.add(email)
        db.commit()
        db.refresh(email)
        process_email_task.delay(email.id)
    return {"synced": True, "fetched": len(messages)}


@router.get("/settings")
def get_settings(db: Session = Depends(get_db)):
    cfg = db.query(SystemConfig).first()
    if not cfg:
        cfg = SystemConfig()
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg


@router.put("/settings")
def put_settings(payload: SettingsUpdate, db: Session = Depends(get_db)):
    cfg = db.query(SystemConfig).first()
    if not cfg:
        cfg = SystemConfig()
        db.add(cfg)
    for key, val in payload.model_dump().items():
        setattr(cfg, key, val)
    db.commit()
    return cfg
