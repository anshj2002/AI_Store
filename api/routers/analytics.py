from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from api.analytics import run_rfm, segment_counts, top_at_risk, recent_negative_mentions, convo_kpis

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.post("/run")
def analytics_run(db: Session = Depends(get_db)):
    result = run_rfm(db)
    return {"ok": True, "result": result}

@router.get("/summary")
def analytics_summary(db: Session = Depends(get_db)):
    return {
        "segments": segment_counts(db),
        "top_risk": top_at_risk(db, limit=10),
        "convo_kpis": convo_kpis(db),
        "recent_negative": recent_negative_mentions(db, limit=5)
    }
