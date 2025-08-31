from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Literal, Optional

from db.database import get_db
from api.models import ContentLog
from api.generation import render_template

router = APIRouter(prefix="/generate", tags=["generate"])

class GenIn(BaseModel):
    topic: str = Field(..., min_length=2)
    audience: str = "general"
    tone: str = "friendly"
    length: Literal["short", "medium", "long"] = "short"
    constraints: Optional[str] = None

class GenOut(BaseModel):
    text: str
    meta: dict

def _log_and_return(db: Session, kind: str, inputs: dict, text: str):
    entry = ContentLog(type=kind, inputs=inputs, output=text)
    db.add(entry)
    db.commit()
    return {"text": text, "meta": {"id": entry.id, "type": kind}}

@router.post("/post", response_model=GenOut)
def generate_post(payload: GenIn, db: Session = Depends(get_db)):
    text = render_template(
        "social_post.md.j2",
        topic=payload.topic,
        audience=payload.audience,
        tone=payload.tone,
        length=payload.length,
        constraints=payload.constraints or ""
    )
    return _log_and_return(db, "post", payload.model_dump(), text)

@router.post("/speech", response_model=GenOut)
def generate_speech(payload: GenIn, db: Session = Depends(get_db)):
    text = render_template(
        "speech.md.j2",
        topic=payload.topic,
        audience=payload.audience,
        tone=payload.tone,
        length=payload.length,
        constraints=payload.constraints or ""
    )
    return _log_and_return(db, "speech", payload.model_dump(), text)

@router.post("/slogan", response_model=GenOut)
def generate_slogan(payload: GenIn, db: Session = Depends(get_db)):
    text = render_template(
        "slogan.md.j2",
        topic=payload.topic,
        audience=payload.audience,
        tone=payload.tone,
        constraints=payload.constraints or ""
    )
    return _log_and_return(db, "slogan", payload.model_dump(), text)
