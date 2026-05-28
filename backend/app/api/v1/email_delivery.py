from pathlib import Path

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from app.core.config import settings
from app.db.session import get_db
from app.models.entities import SystemConfig
from app.services.smtp_sender import send_via_smtp
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/email-delivery", tags=["Email Delivery"])


@router.get("/status")
async def get_delivery_status(db: Session = Depends(get_db)):
    smtp_host_valid = bool(settings.smtp_host and "@" not in settings.smtp_host and "." in settings.smtp_host)
    smtp_ok = bool(settings.smtp_user and settings.smtp_password and smtp_host_valid)
    cfg = db.query(SystemConfig).first()
    gmail_connected = bool(cfg and cfg.gmail_connected)
    return {
        "active_method": settings.email_delivery_mode,
        "smtp_configured": smtp_ok,
        "gmail_api_connected": gmail_connected,
        "real_delivery_active": smtp_ok or gmail_connected,
        "smtp_config": {
            "smtp_host": settings.smtp_host,
            "smtp_port": settings.smtp_port,
            "smtp_user": settings.smtp_user,
            "smtp_host_valid": smtp_host_valid,
        }
        if smtp_ok
        else None,
    }


class TestEmailRequest(BaseModel):
    to_email: EmailStr


@router.post("/test")
async def send_test_email(body: TestEmailRequest):
    return await send_via_smtp(
        to_email=body.to_email,
        to_name="Test User",
        subject="AI Email Delivery Test",
        html_body="""
        <div style="font-family:Arial,sans-serif;max-width:500px;margin:auto;
                    padding:30px;background:#f9f9f9;border-radius:8px">
          <h2 style="color:#059669">Email Delivery is Working!</h2>
          <p>This confirms your SMTP configuration is correct.</p>
          <p>Your AI-powered auto-reply system will now deliver
             real emails to customers' inboxes.</p>
          <hr style="margin:20px 0;border:none;border-top:1px solid #e5e7eb">
          <p style="color:#6b7280;font-size:13px">
            Sent by your AI Email Response System
          </p>
        </div>
        """,
    )


class SmtpConfig(BaseModel):
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    delivery_mode: str = "smtp"


@router.post("/configure-smtp")
async def configure_smtp(config: SmtpConfig):
    env_path = Path(".env")
    env_lines = []
    if env_path.exists():
        env_lines = env_path.read_text(encoding="utf-8").splitlines(keepends=True)

    updates = {
        "EMAIL_DELIVERY_MODE": config.delivery_mode,
        "SMTP_HOST": config.smtp_host,
        "SMTP_PORT": str(config.smtp_port),
        "SMTP_USER": config.smtp_user,
        "SMTP_PASSWORD": config.smtp_password,
    }

    updated_keys = set()
    new_lines = []
    for line in env_lines:
        key = line.split("=")[0].strip()
        if key in updates:
            new_lines.append(f"{key}={updates[key]}\n")
            updated_keys.add(key)
        else:
            new_lines.append(line)

    for key, val in updates.items():
        if key not in updated_keys:
            new_lines.append(f"{key}={val}\n")

    env_path.write_text("".join(new_lines), encoding="utf-8")
    return {
        "success": True,
        "message": "SMTP configured. Restart backend to apply changes.",
        "restart_required": True,
    }
