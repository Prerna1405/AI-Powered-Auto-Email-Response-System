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
