from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _uuid() -> str:
    return str(uuid4())


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    message_id: Mapped[str | None] = mapped_column(String, nullable=True)
    from_email: Mapped[str] = mapped_column(String, nullable=False)
    from_name: Mapped[str | None] = mapped_column(String, nullable=True)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String, default="unprocessed")
    ticket_id: Mapped[str | None] = mapped_column(String, nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ai_analysis: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    transport_mode: Mapped[str] = mapped_column(String, default="simulator")


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    category: Mapped[str] = mapped_column(String, nullable=False)
    intent: Mapped[str] = mapped_column(String, nullable=False, index=True)
    keywords: Mapped[list[str]] = mapped_column(JSON, default=list)
    problem_summary: Mapped[str] = mapped_column(Text, nullable=False)
    solution_template: Mapped[str] = mapped_column(Text, nullable=False)
    variables_used: Mapped[list[str]] = mapped_column(JSON, default=list)
    confidence_threshold: Mapped[int] = mapped_column(Integer, default=75)
    use_count: Mapped[int] = mapped_column(Integer, default=0)
    success_rate: Mapped[float] = mapped_column(Float, default=1.0)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AutoReply(Base):
    __tablename__ = "auto_replies"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    email_id: Mapped[str] = mapped_column(ForeignKey("emails.id"), nullable=False)
    kb_id: Mapped[str | None] = mapped_column(ForeignKey("knowledge_base.id"), nullable=True)
    generated_reply: Mapped[str] = mapped_column(Text, nullable=False)
    ai_confidence: Mapped[int] = mapped_column(Integer, default=0)
    match_method: Mapped[str] = mapped_column(String, default="none")
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    delivery_status: Mapped[str] = mapped_column(String, default="sent")
    delivery_method: Mapped[str] = mapped_column(String(20), default="simulator")
    real_delivered: Mapped[bool] = mapped_column(Boolean, default=False)
    delivery_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_used: Mapped[str] = mapped_column(String, default="gpt-4o")
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)

    email = relationship("Email")


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    ticket_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email_id: Mapped[str] = mapped_column(ForeignKey("emails.id"), nullable=False)
    category: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="open")
    auto_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    escalated_reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class SystemConfig(Base):
    __tablename__ = "system_config"

    id: Mapped[str] = mapped_column(String, primary_key=True, default="default")
    company_name: Mapped[str] = mapped_column(String, default="Acme")
    support_email: Mapped[str] = mapped_column(String, default="support@company.com")
    gmail_connected: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_reply_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    confidence_threshold: Mapped[int] = mapped_column(Integer, default=75)
    signature_template: Mapped[str] = mapped_column(
        Text, default="Best regards,\n{{company_name}} Support Team"
    )
    logo_url: Mapped[str] = mapped_column(String, default="")
    email_poll_interval_seconds: Mapped[int] = mapped_column(Integer, default=60)
