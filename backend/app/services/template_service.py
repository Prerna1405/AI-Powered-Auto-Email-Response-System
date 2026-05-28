from datetime import datetime
from string import Template


def fill_template(raw_template: str, variables: dict[str, str]) -> str:
    normalized = raw_template.replace("{{", "${").replace("}}", "}")
    return Template(normalized).safe_substitute(**variables)


def build_html_reply(
    subject: str,
    customer_name: str,
    body_content: str,
    ticket_id: str,
    company_name: str,
    logo_url: str = "",
) -> str:
    empathy = "We understand how frustrating this can be."
    return f"""
<div style="font-family:Arial,sans-serif;max-width:700px;margin:auto;border:1px solid #e5e7eb">
  <div style="padding:16px;border-bottom:1px solid #e5e7eb">
    <img src="{logo_url}" alt="{company_name}" style="max-height:40px"/>
  </div>
  <div style="padding:16px">
    <p><strong>Subject:</strong> Re: {subject}</p>
    <p>Dear {customer_name or "Customer"},</p>
    <p>{empathy}</p>
    <div>{body_content.replace(chr(10), "<br/>")}</div>
    <p>If you need more help, simply reply to this email.</p>
    <p>Ticket ID: {ticket_id}<br/>Date: {datetime.utcnow().strftime("%Y-%m-%d")}</p>
    <p>Best regards,<br/>{company_name} Support Team</p>
  </div>
  <div style="padding:12px;border-top:1px solid #e5e7eb;color:#6b7280;font-size:12px">
    <a href="#">Unsubscribe</a> | <a href="#">Privacy</a>
  </div>
</div>
"""
