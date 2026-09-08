"""Router Agent tools: read the emotional temperature and the risk words."""

import re

ANGRY = ["furious", "angry", "outrageous", "unacceptable", "ridiculous", "disgusted",
         "worst", "terrible", "appalling", "scam", "fraud", "livid", "fed up", "sick of"]
FRUSTRATED = ["frustrated", "annoyed", "still not", "again", "third time", "twice now",
              "no response", "waiting", "broken", "keeps failing", "stuck", "urgent", "asap"]
POSITIVE = ["thanks", "thank you", "great", "love", "appreciate", "happy", "please"]

# words that raise priority regardless of tone
PRIORITY_KEYWORDS = {
    "refund": "refund", "chargeback": "refund", "charged twice": "refund",
    "double charge": "refund", "duplicate charge": "refund", "money back": "refund",
    "cancel": "churn", "cancelling": "churn", "cancellation": "churn",
    "downgrade": "churn", "switch to a competitor": "churn", "leaving": "churn",
    "legal": "legal", "lawyer": "legal", "attorney": "legal", "gdpr": "legal",
    "sue": "legal", "compliance": "legal", "data breach": "legal",
    "outage": "impact", "down for everyone": "impact", "production": "impact",
}


def detect_sentiment(text: str) -> dict:
    low = text.lower()
    hits_angry = [w for w in ANGRY if w in low]
    hits_frustrated = [w for w in FRUSTRATED if w in low]
    hits_positive = [w for w in POSITIVE if w in low]
    shouting = len(re.findall(r"\b[A-Z]{4,}\b", text)) >= 2

    if hits_angry or shouting:
        label = "angry"
    elif hits_frustrated:
        label = "frustrated"
    elif hits_positive and not hits_frustrated:
        label = "positive"
    else:
        label = "neutral"

    return {
        "sentiment": label,
        "matched": (hits_angry + hits_frustrated + hits_positive)[:5],
        "shouting": shouting,
    }


def check_priority_keywords(text: str) -> dict:
    low = text.lower()
    matched = {kw: kind for kw, kind in PRIORITY_KEYWORDS.items() if kw in low}
    kinds = set(matched.values())

    if kinds & {"legal", "refund"}:
        priority = "high"
    elif kinds & {"churn", "impact"}:
        priority = "medium"
    else:
        priority = "normal"

    return {
        "priority": priority,
        "matched": sorted(matched),
        "kinds": sorted(kinds),
        "refund_intent": "refund" in kinds,
    }
