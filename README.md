# AI-Powered Automatic Email Response System

Production-ready full-stack system that ingests support emails, detects intent with AI, matches a knowledge-base solution, and sends professional HTML replies automatically.

## Features
- FastAPI backend with PostgreSQL persistence
- Celery + Redis async processing pipeline
- Dual transport mode:
  - Gmail mode (OAuth-ready toggle points and API stubs)
  - Simulator mode (works immediately with no Gmail setup)
- Knowledge base CRUD with 20+ seeded intents
- AI pipeline:
  1. Ingestion
  2. Intent analysis
  3. KB matching (exact + TF-IDF fallback)
  4. Template personalization + HTML rendering
  5. Reply send + ticket/status logging
- Gmail-style frontend (Inbox, Dashboard, KB, Preview, Analytics, Settings)
- Docker Compose for full local stack

## Folder Structure
```text
ai-powered-automatic-email-response-system/
  backend/
    app/
      api/
      core/
      db/
      models/
      schemas/
      seed/
      services/
      workers/
    migrations/
    tests/
  frontend/
    src/
      api/
      components/
      pages/
      types/
  docker-compose.yml
```

## Quick Start (Simulator Mode)
1. `docker compose up --build`
2. Backend API: `http://localhost:8000/docs`
3. Frontend UI: `http://localhost:5173`
4. Open Inbox page, compose a support email, send, and observe auto-reply lifecycle.

## Local Dev (without Docker)
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Worker
```bash
cd backend
celery -A app.workers.tasks worker --loglevel=info
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Gmail Mode Setup
1. Enable Gmail API in Google Cloud.
2. Configure OAuth credentials.
3. Set env values:
   - `GMAIL_CLIENT_ID`
   - `GMAIL_CLIENT_SECRET`
   - `GMAIL_REFRESH_TOKEN`
4. Update `/api/settings` or call `/api/gmail/connect` to enable Gmail mode.

> Current implementation includes Gmail mode switch points and status APIs. Plug full Gmail fetch/send into `mail_transport.py` and scheduler task in workers for production OAuth flow.

## API Coverage
Implemented endpoints:
- `/api/emails/*`
- `/api/kb/*`
- `/api/analytics/*`
- `/api/gmail/*`
- `/api/settings`

## Testing
```bash
cd backend
pytest
```
=======
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
CONFIDENCE_THRESHOLD=70      
  
