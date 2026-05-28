from app.services.gmail_service import send_via_gmail


async def send_via_gmail_api(to_email: str, to_name: str, subject: str, html_body: str) -> dict:
    _ = to_name
    result = send_via_gmail(to_email, subject, html_body)
    return {"success": bool(result.get("sent")), **result}
