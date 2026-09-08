"""Evaluator - the control node. Scores the draft; its score drives the escalation edge."""

import re
import time

from llm import LLMError, call_llm_json, warn_fallback
from state import SupportState
from trace import span

CONFIDENCE_THRESHOLD = 0.60
STRONG_DOC_SCORE = 4.0

SYSTEM = """You grade a drafted support reply. Be strict.

Score 0.0-1.0 on: does it actually answer the ticket, is every claim backed by the supplied
context, would a support lead send it unedited.

0.9+ answers completely and cites records. 0.5 partially answers. Below 0.4 is vague, generic,
or asks the customer to clarify.

Reply with JSON only: {"score": 0.0, "note": "<12 words max>"}"""

STOPWORDS = {"the", "and", "with", "that", "this", "have", "from", "your", "just", "been",
             "when", "what", "why", "how", "does", "did", "for", "you", "our", "not"}


def evaluator(state: SupportState) -> dict:
    t0 = time.perf_counter()
    draft = state.get("draft", "")
    notes = []

    deterministic = _deterministic_score(state, draft, notes)

    try:
        data = call_llm_json(SYSTEM, f"Ticket: {state['ticket']}\n\nDraft reply:\n{draft}",
                             temperature=0.0)
        llm_score = max(0.0, min(1.0, float(data.get("score", 0))))
        notes.append(f"judge {llm_score:.2f}: {str(data.get('note', ''))[:60]}")
        confidence = round(0.6 * deterministic + 0.4 * llm_score, 2)
    except (LLMError, TypeError, ValueError) as exc:
        warn_fallback("Evaluator", exc)
        notes.append("judge unavailable, deterministic score only")
        confidence = round(deterministic, 2)

    verdict = "HIGH" if confidence >= CONFIDENCE_THRESHOLD else "LOW"
    return {
        "confidence": confidence,
        "eval_notes": notes,
        "trace": [span("Evaluator", t0, f"draft {len(draft)} chars",
                       f"confidence {confidence:.2f} {verdict} ({'; '.join(notes)})")],
    }


def _deterministic_score(state: SupportState, draft: str, notes: list[str]) -> float:
    docs = state.get("docs") or []
    facts = state.get("account_facts") or {}
    diagnosis = state.get("diagnosis") or {}

    strong = facts.get("found") or diagnosis.get("error") or (
        docs and docs[0]["score"] >= STRONG_DOC_SCORE)
    score = 0.35 if strong else (0.15 if docs else 0.0)
    notes.append("strong sources" if strong else ("weak sources" if docs else "no sources"))

    ticket_words = _content_words(state["ticket"])
    draft_words = _content_words(draft)
    coverage = (len(ticket_words & draft_words) / len(ticket_words)) if ticket_words else 0.0
    score += 0.20 * coverage

    if len(ticket_words) >= 6:
        score += 0.20
    elif len(ticket_words) >= 3:
        score += 0.10
    else:
        notes.append("ticket too vague to verify an answer")

    if not state.get("tone_flags"):
        score += 0.10
    if state.get("category") != "unclear":
        score += 0.15

    return min(score, 1.0)


def _content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9_]{3,}", text.lower()) if w not in STOPWORDS}


def route_after_eval(state: SupportState) -> str:
    """The conditional edge: escalate on low confidence, refunds, anger or legal risk."""
    if state.get("confidence", 0) < CONFIDENCE_THRESHOLD:
        return "escalate"
    if state.get("category") == "refund":
        return "escalate"
    if state.get("sentiment") == "angry":
        return "escalate"
    if state.get("priority") == "high":
        return "escalate"
    return "respond"
