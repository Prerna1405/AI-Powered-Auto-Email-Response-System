from datetime import datetime
from time import perf_counter, sleep
from sqlalchemy.orm import Session

from app.models.entities import AutoReply
from app.models.entities import Email, Ticket
from app.services.ai_service import analyze_intent, personalize_reply
from app.services.email_delivery import deliver_reply
from app.services.kb_matcher import match_kb_article
from app.services.template_service import build_html_reply, fill_template
from app.services.ticketing import generate_ticket_number


def process_email(db: Session, email_id: str) -> dict:
    started = perf_counter()
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        return {"ok": False, "reason": "email_not_found"}

    email.status = "processing"
    db.commit()
    # Keep a short processing window so simulator UI can show "Processing...".
    sleep(1.2)

    analysis = analyze_intent(email.subject, email.body)
    email.ai_analysis = analysis
    if analysis.get("is_spam"):
        email.status = "failed"
        db.commit()
        return {"ok": True, "status": "spam_ignored"}

    ticket_number = generate_ticket_number()
    email.ticket_id = ticket_number
    ticket = db.query(Ticket).filter(Ticket.email_id == email.id).first()
    if not ticket:
        ticket = Ticket(
            ticket_number=ticket_number,
            email_id=email.id,
            category=analysis.get("category"),
            status="processing",
            auto_resolved=False,
        )
        db.add(ticket)
    db.commit()

    article, match_method = match_kb_article(db, analysis, f"{email.subject} {email.body}")
    confidence = int(analysis.get("confidence", 0))
    threshold = article.confidence_threshold if article else 75

    if not article or confidence < threshold:
        email.status = "escalated"
        ticket.status = "escalated"
        ticket.escalated_reason = "low_confidence_or_no_match"
        db.commit()
        return {"ok": True, "status": "escalated"}

    variables = {
        "customer_name": analysis.get("extracted_name") or email.from_name or "Customer",
        "company_name": "Acme",
        "ticket_id": ticket_number,
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "reset_url": "https://example.com/reset-password",
    }
    rendered = fill_template(article.solution_template, variables)
    personalized = personalize_reply(
        rendered,
        {
            "sentiment": analysis.get("sentiment", "neutral"),
            "name": variables["customer_name"],
            "summary": analysis.get("summary", ""),
        },
    )
    html = build_html_reply(email.subject, variables["customer_name"], personalized, ticket_number, "Acme")
    delivery = _run_async_delivery(
        deliver_reply(
            to_email=email.from_email,
            to_name=email.from_name or variables["customer_name"],
            subject=f"Re: {email.subject}",
            html_body=html,
            db=db,
        )
    )
    db.add(
        AutoReply(
            email_id=email.id,
            kb_id=article.id if article else None,
            generated_reply=html,
            ai_confidence=confidence,
            match_method=match_method,
            delivery_status="sent" if delivery["delivered"] else "simulated",
            delivery_method=delivery["method"],
            real_delivered=delivery["delivered"],
            delivery_error=delivery.get("error"),
            model_used="gpt-4o",
            tokens_used=0,
        )
    )
    email.status = "replied"
    ticket.status = "auto_resolved"
    ticket.auto_resolved = True
    email.processing_time_ms = int((perf_counter() - started) * 1000)
    db.commit()
    return {
        "ok": True,
        "status": "replied",
        "transport": delivery["method"],
        "real_delivered": delivery["delivered"],
        "match_method": match_method,
    }


def _run_async_delivery(coro):
    import asyncio

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    if loop.is_running():
        new_loop = asyncio.new_event_loop()
        try:
            return new_loop.run_until_complete(coro)
        finally:
            new_loop.close()
    return loop.run_until_complete(coro)
