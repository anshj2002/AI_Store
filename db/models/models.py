from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP
from sqlalchemy.sql import func

# Import Base from database.py to share the same declarative base
from db.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    confidence_score = Column(Float)
    timestamp = Column(TIMESTAMP, server_default=func.now())
