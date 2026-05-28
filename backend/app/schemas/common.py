from datetime import datetime
from pydantic import BaseModel, Field


class EmailCreate(BaseModel):
    from_email: str
    from_name: str | None = None
    subject: str
    body: str
    message_id: str | None = None
    transport_mode: str = "simulator"


class EmailOut(BaseModel):
    id: str
    from_email: str
    from_name: str | None
    subject: str
    body: str
    status: str
    ticket_id: str | None
    received_at: datetime
    ai_analysis: dict | None = None

    class Config:
        from_attributes = True


class KBCreate(BaseModel):
    category: str
    intent: str
    keywords: list[str] = Field(default_factory=list)
    problem_summary: str
    solution_template: str
    variables_used: list[str] = Field(default_factory=list)
    confidence_threshold: int = 75


class KBOut(KBCreate):
    id: str
    use_count: int = 0
    success_rate: float = 1

    class Config:
        from_attributes = True


class SettingsUpdate(BaseModel):
    company_name: str
    support_email: str
    gmail_connected: bool
    auto_reply_enabled: bool
    confidence_threshold: int
    signature_template: str
    logo_url: str
    email_poll_interval_seconds: int
