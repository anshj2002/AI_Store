from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional

from db.database import get_db
from db.models.models import Message
from api.models import Feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])

class FeedbackIn(BaseModel):
    message_id: int = Field(..., ge=1)
    helpful: bool
    comment: Optional[str] = None

@router.post("")
def submit_feedback(payload: FeedbackIn, db: Session = Depends(get_db)):
    # Optional: verify message exists (soft check; skip FK for MVP)
    msg = db.get(Message, payload.message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="message_id not found")

    fb = Feedback(
        message_id=payload.message_id,
        helpful=payload.helpful,
        comment=payload.comment
    )
    db.add(fb)
    db.commit()
    return {"ok": True, "feedback_id": fb.id}
