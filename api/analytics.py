from __future__ import annotations
import os
import math
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import text

from api.models import CustomerScore

# CSV location (mount a 'data' folder at project root)
CUSTOMERS_CSV = os.path.join(os.path.dirname(__file__), "../data/customers.csv")


def _now_utc():
    return datetime.now(timezone.utc)

def _days_since(date_str: str | None) -> int:
    if not date_str or str(date_str).strip() == "":
        return 10_000
    try:
        d = datetime.fromisoformat(str(date_str)).replace(tzinfo=None)
        return max(0, (datetime.utcnow() - d).days)
    except Exception:
        return 10_000

def _bucket_recency(days: int) -> int:
    # R: lower days -> higher score
    if days <= 30: return 5
    if days <= 60: return 4
    if days <= 120: return 3
    if days <= 240: return 2
    return 1

def _bucket_frequency(n: int) -> int:
    if n > 20: return 5
    if n >= 11: return 4
    if n >= 6: return 3
    if n >= 2: return 2
    return 1

def _bucket_monetary(x: float) -> int:
    if x > 50_000: return 5
    if x >= 20_000: return 4
    if x >= 10_000: return 3
    if x >= 2_000: return 2
    return 1

def _sigmoid(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))

def _propensity(r: int, f: int, m: int) -> float:
    z = 0.8 * r + 0.6 * f + 0.7 * m - 6.0
    return round(_sigmoid(z), 4)

def _segment(r: int, f: int, m: int, joined_at: str | None, days_since_last: int) -> str:
    try:
        joined_days = _days_since(joined_at)
    except Exception:
        joined_days = 10_000
    if r >= 4 and (f >= 4 or m >= 4):
        return "Champions"
    if r >= 3 and f >= 3 and m >= 3:
        return "Loyal"
    if r <= 2 and (f <= 2 or m <= 2) and joined_days > 180:
        return "At-Risk"
    if f <= 2 and r <= 2:
        return "Hibernating"
    return "New"

def run_rfm(db: Session) -> dict:
    if not os.path.exists(CUSTOMERS_CSV):
        raise FileNotFoundError(f"customers.csv not found at {CUSTOMERS_CSV}")

    df = pd.read_csv(CUSTOMERS_CSV)
    req_cols = {"id","name","email","joined_at","city","age","last_purchase_at","total_orders","total_spend"}
    missing = req_cols - set(df.columns)
    if missing:
        raise ValueError(f"customers.csv missing columns: {sorted(missing)}")

    # Compute R, F, M per row
    rows = []
    for _, r in df.iterrows():
        days = _days_since(str(r.get("last_purchase_at")))
        r_score = _bucket_recency(days)
        f_score = _bucket_frequency(int(r.get("total_orders", 0)))
        m_score = _bucket_monetary(float(r.get("total_spend", 0.0)))
        prop = _propensity(r_score, f_score, m_score)
        seg = _segment(r_score, f_score, m_score, str(r.get("joined_at")), days)
        rows.append({
            "user_id": str(r["id"]),
            "r_score": r_score,
            "f_score": f_score,
            "m_score": m_score,
            "propensity": float(prop),
            "segment": seg
        })

    # Replace all rows (simple MVP: truncate + insert)
    db.execute(text("DELETE FROM customer_scores"))
    for row in rows:
        db.add(CustomerScore(**row))
    db.commit()

    # Return quick counts
    seg_counts = {}
    for row in rows:
        seg_counts[row["segment"]] = seg_counts.get(row["segment"], 0) + 1

    return {
        "total": len(rows),
        "segments": seg_counts
    }

def convo_kpis(db: Session) -> dict:
    # Aggregate from messages + feedback
    # total, escalation_rate (< threshold), avg_confidence, helpful_rate
    threshold = 30.0  # Default confidence threshold
    total = db.execute(text("SELECT COUNT(*) FROM messages")).scalar_one()
    low = db.execute(text("SELECT COUNT(*) FROM messages WHERE confidence IS NOT NULL AND confidence < :t"), {"t": threshold}).scalar_one()
    avg_conf = db.execute(text("SELECT AVG(confidence) FROM messages")).scalar_one() or 0.0

    # helpful rate
    fb_total = db.execute(text("SELECT COUNT(*) FROM feedback")).scalar_one()
    fb_help = db.execute(text("SELECT COUNT(*) FROM feedback WHERE helpful = TRUE")).scalar_one()
    helpful_rate = (fb_help / fb_total) if fb_total else None

    return {
        "total": int(total),
        "escalation_rate": round((low / total), 4) if total else 0.0,
        "avg_confidence": round(float(avg_conf), 4) if avg_conf else 0.0,
        "helpful_rate": round(float(helpful_rate), 4) if helpful_rate is not None else None
    }

def segment_counts(db: Session) -> dict:
    rows = db.execute(text("SELECT segment, COUNT(*) FROM customer_scores GROUP BY segment")).all()
    return {seg: int(c) for seg, c in rows}

def top_at_risk(db: Session, limit: int = 10) -> list[dict]:
    q = text("""
        SELECT user_id, r_score, f_score, m_score, propensity, segment
        FROM customer_scores
        ORDER BY propensity ASC, r_score ASC
        LIMIT :lim
    """)
    res = db.execute(q, {"lim": limit}).mappings().all()
    return [dict(r) for r in res]

def recent_negative_mentions(db: Session, limit: int = 5) -> list[dict]:
    # May not exist yet; handle gracefully
    try:
        q = text("""
          SELECT title, source, url, sentiment, topic
          FROM mentions
          WHERE sentiment <= -0.6 OR (is_misinfo = TRUE)
          ORDER BY created_at DESC
          LIMIT :lim
        """)
        res = db.execute(q, {"lim": limit}).mappings().all()
        return [dict(r) for r in res]
    except Exception:
        return []
