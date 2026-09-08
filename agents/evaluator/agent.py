"""Evaluator - the control node. Scores the merged draft; its score drives the escalation edge."""

import re
import time

from agents.evaluator.tools import judge_answer, score_sources
from llm import LLMError, warn_fallback
from state import SupportState
from trace import record, span

CONFIDENCE_THRESHOLD = 0.60

STOPWORDS = {"the", "and", "with", "that", "this", "have", "from", "your", "just", "been",
             "when", "what", "why", "how", "does", "did", "for", "you", "our", "not"}


def evaluator(state: SupportState) -> dict:
    t0 = time.perf_counter()
    draft = state.get("draft", "")
    results = state.get("results") or []
    notes = []

    source_score, source_note = score_sources(results)
    notes.append(source_note)
    calls = [record("score_sources", {"results": len(results)},
                    f"{source_note} ({source_score:.2f})")]

    deterministic = source_score + _writing_score(state, draft, notes)

    try:
        llm_score, llm_note = judge_answer(state["ticket"], draft)
        notes.append(f"judge {llm_score:.2f}: {llm_note}")
        confidence = round(0.6 * deterministic + 0.4 * llm_score, 2)
    except LLMError as exc:
        warn_fallback("Evaluator", exc)
        notes.append("judge unavailable, deterministic score only")
        confidence = round(deterministic, 2)
    calls.append(record("judge_answer", {"draft_chars": len(draft)}, notes[-1]))

    verdict = "HIGH" if confidence >= CONFIDENCE_THRESHOLD else "LOW"
    return {
        "confidence": confidence,
        "eval_notes": notes,
        "tool_calls": calls,
        "trace": [span("Evaluator", t0, f"draft {len(draft)} chars",
                       f"confidence {confidence:.2f} {verdict} ({'; '.join(notes)})")],
    }


def _writing_score(state: SupportState, draft: str, notes: list[str]) -> float:
    """The other 0.65: does the draft cover the mail, was the mail answerable, is the tone ok."""
    ticket_words = _content_words(state["ticket"])
    coverage = (len(ticket_words & _content_words(draft)) / len(ticket_words)
                if ticket_words else 0.0)
    score = 0.20 * coverage

    if len(ticket_words) >= 6:
        score += 0.20
    elif len(ticket_words) >= 3:
        score += 0.10
    else:
        notes.append("mail too vague to verify an answer")

    if not state.get("tone_flags"):
        score += 0.10
    if state.get("category") != "unclear":
        score += 0.15
    return score


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
