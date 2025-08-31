from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from db.database import get_db
from db.models.models import Message
from api.faq_service import FAQService

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    confidence_score: Optional[float] = None
    message_id: Optional[int] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """Handle chat requests and return AI responses"""
    try:
        # Initialize FAQ service
        faq_service = FAQService(db)

        # Find best matching FAQ
        response, confidence = faq_service.find_best_match(request.message)

        if not response:
            response = faq_service.get_fallback_response()
            confidence = 0.0

        # Save message to database
        db_message = Message(
            user_message=request.message,
            bot_response=response,
            confidence_score=confidence
        )

        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        return ChatResponse(
            response=response,
            confidence_score=confidence,
            message_id=db_message.id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@router.get("/messages")
async def get_messages(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent chat messages"""
    try:
        messages = db.query(Message).order_by(Message.timestamp.desc()).limit(limit).all()
        return [
            {
                "id": msg.id,
                "user_message": msg.user_message,
                "bot_response": msg.bot_response,
                "confidence_score": msg.confidence_score,
                "timestamp": msg.timestamp
            }
            for msg in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {str(e)}")
