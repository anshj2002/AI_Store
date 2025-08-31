from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from .models import FAQ
import re
from collections import Counter

class FAQService:
    def __init__(self, db: Session):
        self.db = db

    def preprocess_text(self, text: str) -> List[str]:
        """Preprocess text by removing punctuation and converting to lowercase"""
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text.split()

    def calculate_confidence(self, user_words: List[str], faq_keywords: List[str]) -> float:
        """Calculate confidence score based on keyword matching"""
        if not faq_keywords or not user_words:
            return 0.0

        # Count matches
        user_counter = Counter(user_words)
        keyword_counter = Counter(faq_keywords)

        # Calculate intersection
        matches = sum((user_counter & keyword_counter).values())
        total_keywords = len(faq_keywords)

        if total_keywords == 0:
            return 0.0

        # Return confidence as a percentage
        confidence = (matches / total_keywords) * 100
        return min(confidence, 100.0)  # Cap at 100%

    def find_best_match(self, user_message: str) -> Tuple[Optional[str], float]:
        """Find the best matching FAQ with confidence score"""
        user_words = self.preprocess_text(user_message)

        # Get all FAQs from database
        faqs = self.db.query(FAQ).all()

        best_match = None
        best_confidence = 0.0

        for faq in faqs:
            confidence = self.calculate_confidence(user_words, faq.keywords_list)

            if confidence > best_confidence:
                best_confidence = confidence
                best_match = faq.answer

        # Only return match if confidence is above threshold
        if best_confidence > 0.0:  # Any match
            return best_match, best_confidence

        return None, 0.0

    def get_fallback_response(self) -> str:
        """Return a fallback response when no FAQ matches"""
        return "I'm sorry, I couldn't find a specific answer to your question. Please contact our support team for assistance."
