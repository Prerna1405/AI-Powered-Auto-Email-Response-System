import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.entities import SystemConfig
from app.services.smtp_sender import send_via_smtp

logger = logging.getLogger(__name__)


def get_system_config(db: Session) -> SystemConfig | None:
    return db.query(SystemConfig).first()


async def deliver_reply(
    to_email: str,
    to_name: str,
    subject: str,
    html_body: str,
    db: Session,
) -> dict:
    if settings.email_delivery_mode == "gmail_api":
        from app.services.gmail_api import send_via_gmail_api

        config = get_system_config(db)
        if config and config.gmail_connected:
            result = await send_via_gmail_api(to_email, to_name, subject, html_body)
            if result.get("success"):
                return {**result, "delivered": True, "method": "gmail_api"}
        logger.warning("Gmail API not connected. Falling back to SMTP.")

    if settings.smtp_user and settings.smtp_password:
        result = await send_via_smtp(to_email, to_name, subject, html_body)
        if result.get("success"):
            return {**result, "delivered": True, "method": "smtp"}
        logger.warning("SMTP failed: %s. Falling back to simulator.", result.get("error", "unknown"))

    logger.info("Simulator mode. Reply saved to DB only for %s", to_email)
    return {
        "delivered": False,
        "method": "simulator",
        "to_email": to_email,
        "message": "Reply saved in app only. To send real emails: add SMTP credentials to .env",
    }
