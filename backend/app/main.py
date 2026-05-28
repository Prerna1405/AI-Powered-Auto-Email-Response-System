from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.routes import router
from app.api.v1.email_delivery import router as delivery_router
from app.db.session import Base, SessionLocal, engine
from app.models.entities import KnowledgeBase, SystemConfig
from app.seed.kb_seed import KB_SEED

app = FastAPI(title="AI-Powered Automatic Email Response System")
app.include_router(router)
app.include_router(delivery_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        db.execute(
            text(
                """
                ALTER TABLE auto_replies
                  ADD COLUMN IF NOT EXISTS delivery_method VARCHAR(20) DEFAULT 'simulator',
                  ADD COLUMN IF NOT EXISTS real_delivered BOOLEAN DEFAULT FALSE,
                  ADD COLUMN IF NOT EXISTS delivery_error TEXT
                """
            )
        )
        cfg = db.query(SystemConfig).first()
        if not cfg:
            db.add(SystemConfig())
        if db.query(KnowledgeBase).count() == 0:
            for row in KB_SEED:
                db.add(KnowledgeBase(**row))
        db.commit()
    finally:
        db.close()


@app.get("/health")
def health():
    return {"ok": True}
