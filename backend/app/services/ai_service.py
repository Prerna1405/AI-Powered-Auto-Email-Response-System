import json
from typing import Any

from openai import OpenAI

from app.core.config import settings


def analyze_intent(subject: str, body: str) -> dict[str, Any]:
    if not settings.openai_api_key:
        return _heuristic_analysis(subject, body)

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = f"""
You are an email intent detector for support.
Return strict JSON:
{{
  "intent": "...",
  "category": "...",
  "confidence": 0-100,
  "sentiment": "frustrated|neutral|positive",
  "summary": "...",
  "extracted_name": "...",
  "is_spam": false,
  "requires_human": false
}}
Subject: {subject}
Body: {body}
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)


def personalize_reply(template: str, context: dict[str, Any]) -> str:
    if not settings.openai_api_key:
        return template

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = f"""
Personalize this support reply, keep solution steps intact and professional.
Context: {json.dumps(context)}
Template:
{template}
"""
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content or template


def _heuristic_analysis(subject: str, body: str) -> dict[str, Any]:
    text = f"{subject} {body}".lower()
    if "password" in text or "reset" in text:
        return {
            "intent": "password_reset",
            "category": "Account",
            "confidence": 90,
            "sentiment": "frustrated",
            "summary": "User cannot log in and needs a password reset",
            "extracted_name": "",
            "is_spam": False,
            "requires_human": False,
        }
    if "refund" in text or "cancel" in text:
        return {
            "intent": "refund_request",
            "category": "Billing & Payments",
            "confidence": 82,
            "sentiment": "neutral",
            "summary": "Customer asks for cancellation or refund",
            "extracted_name": "",
            "is_spam": False,
            "requires_human": False,
        }
    return {
        "intent": "general_inquiry",
        "category": "General Inquiry",
        "confidence": 65,
        "sentiment": "neutral",
        "summary": "General support inquiry",
        "extracted_name": "",
        "is_spam": "buy now" in text or "bitcoin" in text,
        "requires_human": False,
    }
