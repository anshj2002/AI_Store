from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import get_db
from api.reputation import analyze_and_store
from api.models import Mention

router = APIRouter(prefix="/reputation", tags=["reputation"])

class RepIn(BaseModel):
    title: str
    text: str | None = None
    url: str | None = None
    source: str | None = None

class RepOut(BaseModel):
    sentiment: float
    topic: str
    is_misinfo: bool
    suggestion: str

@router.post("/analyze", response_model=RepOut)
def analyze(payload: RepIn, db: Session = Depends(get_db)):
    m = analyze_and_store(db, payload.source, payload.url, payload.title, payload.text)
    return RepOut(
        sentiment=m.sentiment,
        topic=m.topic,
        is_misinfo=m.is_misinfo,
        suggestion=m.suggestion,
    )

@router.get("/summary")
def reputation_summary(db: Session = Depends(get_db)):
    rows = db.query(Mention).order_by(Mention.created_at.desc()).limit(10).all()
    return [
        {
            "title": r.title,
            "source": r.source,
            "url": r.url,
            "sentiment": r.sentiment,
            "topic": r.topic,
            "is_misinfo": r.is_misinfo,
            "suggestion": r.suggestion,
            "created_at": r.created_at
        }
        for r in rows
    ]
