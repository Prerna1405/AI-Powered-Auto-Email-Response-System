import logging
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_via_smtp(to_email: str, to_name: str, subject: str, html_body: str) -> dict:
    try:
        if "@" in settings.smtp_host or "." not in settings.smtp_host:
            return {
                "success": False,
                "method": "smtp",
                "error": f"Invalid SMTP_HOST: {settings.smtp_host}",
                "fix": "Use an SMTP server host, e.g. smtp.gmail.com",
            }

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{settings.company_name} Support <{settings.smtp_user}>"
        msg["To"] = f"{to_name} <{to_email}>"

        plain_text = html_body.replace("<br>", "\n").replace("</p>", "\n")
        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        if settings.smtp_port == 465:
            with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
                server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.smtp_user, to_email, msg.as_string())
        else:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.smtp_user, to_email, msg.as_string())

        logger.info("SMTP delivered to %s", to_email)
        return {"success": True, "method": "smtp", "to": to_email}
    except smtplib.SMTPAuthenticationError:
        return {
            "success": False,
            "method": "smtp",
            "error": "Authentication failed. Check SMTP_USER and SMTP_PASSWORD.",
            "fix": "For Gmail: use App Password not your Gmail password.",
        }
    except smtplib.SMTPRecipientsRefused:
        return {
            "success": False,
            "method": "smtp",
            "error": f"Recipient refused: {to_email}",
        }
    except socket.gaierror:
        return {
            "success": False,
            "method": "smtp",
            "error": "DNS lookup failed for SMTP host.",
            "fix": "Set SMTP_HOST to a valid server like smtp.gmail.com",
        }
    except Exception as exc:
        return {"success": False, "method": "smtp", "error": str(exc)}
