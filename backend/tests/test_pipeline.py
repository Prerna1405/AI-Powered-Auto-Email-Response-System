from app.services.ai_service import _heuristic_analysis
from app.services.template_service import fill_template
from app.services.ticketing import generate_ticket_number


def test_ticket_format():
    ticket = generate_ticket_number()
    assert ticket.startswith("TKT-")


def test_heuristic_detects_password_reset():
    out = _heuristic_analysis("Need password reset", "I forgot my password")
    assert out["intent"] == "password_reset"
    assert out["confidence"] >= 80


def test_template_filling():
    text = "Hello {{customer_name}}, ticket={{ticket_id}}"
    rendered = fill_template(text, {"customer_name": "John", "ticket_id": "TKT-123"})
    assert "John" in rendered
    assert "TKT-123" in rendered
