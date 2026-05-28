# AI-Powered-Auto-Email-Response-System
AI-powered support email automation platform with FastAPI, Celery, PostgreSQL, and React; classifies incoming emails, matches knowledge-base solutions, and sends professional auto-replies via SMTP/Gmail with simulator fallback.

# ── Database ─────────────────────────────────────────
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/emailbot

# ── Redis / Celery ────────────────────────────────────
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# ── Auth ─────────────────────────────────────────────
JWT_SECRET=your_secret_key_here
JWT_EXPIRE_MINUTES=15
REFRESH_EXPIRE_DAYS=7

# ── OpenAI ───────────────────────────────────────────
OPENAI_API_KEY=sk-your-openai-key

# ── Email Delivery ────────────────────────────────────
EMAIL_DELIVERY_MODE=simulator   # simulator | smtp | gmail_api
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=
SMTP_PASSWORD=
COMPANY_NAME=SupportBot

# ── AI Thresholds ────────────────────────────────────
CONFIDENCE_THRESHOLD=70         # below this → escalate to human
