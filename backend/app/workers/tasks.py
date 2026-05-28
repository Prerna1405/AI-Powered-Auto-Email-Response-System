from app.db.session import SessionLocal
from app.services.pipeline import process_email
from app.workers.celery_app import celery_app


@celery_app.task(name="process_email_task")
def process_email_task(email_id: str):
    db = SessionLocal()
    try:
        return process_email(db, email_id)
    finally:
        db.close()
