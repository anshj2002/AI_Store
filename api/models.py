from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, Float, TIMESTAMP
from sqlalchemy.sql import func
from db.database import Base
import json

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    keywords = Column(String, nullable=False)  # Store as JSON string
    created_at = Column(TIMESTAMP, server_default=func.now())

    @property
    def keywords_list(self):
        return json.loads(self.keywords) if self.keywords else []

    @keywords_list.setter
    def keywords_list(self, value):
        self.keywords = json.dumps(value)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, index=True)  # keep simple (no FK for MVP)
    helpful = Column(Boolean, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ContentLog(Base):
    __tablename__ = "content_log"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)  # 'post' | 'speech' | 'slogan'
    inputs = Column(JSON)
    output = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CustomerScore(Base):
    __tablename__ = "customer_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    r_score = Column(Integer, nullable=False)
    f_score = Column(Integer, nullable=False)
    m_score = Column(Integer, nullable=False)
    propensity = Column(Float, nullable=False)
    segment = Column(String, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

class Mention(Base):
    __tablename__ = "mentions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sentiment: Mapped[float] = mapped_column(Float)
    topic: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_misinfo: Mapped[bool] = mapped_column(default=False)
    suggestion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
