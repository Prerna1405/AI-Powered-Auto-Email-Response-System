from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app.models.entities import KnowledgeBase


def match_kb_article(db: Session, analysis: dict[str, Any], text: str) -> tuple[KnowledgeBase | None, str]:
    intent = analysis.get("intent", "")
    exact = db.query(KnowledgeBase).filter(KnowledgeBase.intent == intent).first()
    if exact:
        return exact, "exact_intent"

    kb_items = db.query(KnowledgeBase).all()
    if not kb_items:
        return None, "none"

    corpus = [" ".join(item.keywords) + " " + item.problem_summary for item in kb_items]
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(corpus + [text.lower()])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    best_idx = scores.argmax()
    if scores[best_idx] > 0.15:
        return kb_items[best_idx], "tfidf"
    return None, "none"
