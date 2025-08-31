import re
from sqlalchemy.orm import Session
from api.models import Mention

def simple_sentiment(text: str) -> float:
    if not text:
        return 0.0
    text_l = text.lower()
    negatives = ["fraud","scam","fake","bad","angry","delay","poor","hate","cheat","complaint"]
    positives = ["great","good","happy","fast","love","excellent","smooth","trust","reliable"]
    score = 0
    for w in positives:
        if w in text_l: score += 1
    for w in negatives:
        if w in text_l: score -= 1
    return max(-1.0, min(1.0, score/3.0))

def simple_topic(text: str) -> str:
    if not text: return "general"
    t = text.lower()
    if "delivery" in t: return "delivery"
    if "price" in t or "cost" in t: return "pricing"
    if "support" in t or "service" in t: return "support"
    if "return" in t or "refund" in t: return "returns"
    return "general"

def detect_misinfo(text: str) -> bool:
    if not text: return False
    t = text.lower()
    # crude check: if uncertain claim words exist
    return any(kw in t for kw in ["rumor","fake news","unverified","hoax"])

def make_suggestion(topic: str, sentiment: float, is_misinfo: bool) -> str:
    if is_misinfo:
        return "We recommend clarifying with official facts and directing readers to our verified channels."
    if sentiment <= -0.6:
        return f"Offer an apology and a quick resolution regarding {topic}."
    if sentiment >= 0.6:
        return f"Thank the customer publicly for their positive feedback about {topic}."
    return f"Acknowledge the comment about {topic} and provide helpful context."

def analyze_and_store(db: Session, source: str | None, url: str | None, title: str, text: str) -> Mention:
    s = simple_sentiment(text or title or "")
    t = simple_topic(text or title or "")
    misinfo = detect_misinfo(text or title or "")
    sugg = make_suggestion(t, s, misinfo)

    m = Mention(
        source=source,
        url=url,
        title=title,
        text=text,
        sentiment=s,
        topic=t,
        is_misinfo=misinfo,
        suggestion=sugg,
    )
    db.add(m)
    db.commit()
    return m
