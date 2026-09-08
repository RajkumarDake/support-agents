"""Evaluator tools: how good were the sources, and what does an LLM judge think of the draft."""

from llm import LLMError, call_llm_json

JUDGE_SYSTEM = """You grade a drafted support reply. Be strict.

Score 0.0-1.0 on: does it answer EVERY problem raised in the mail, is every claim backed by the
supplied context, would a support lead send it unedited.

0.9+ answers completely and cites records. 0.5 partially answers. Below 0.4 is vague, generic,
or asks the customer to clarify.

Reply with JSON only: {"score": 0.0, "note": "<12 words max>"}"""


def score_sources(results: list[dict]) -> tuple[float, str]:
    """0.35 of the confidence score comes from what the specialists actually found."""
    if any(r["strong"] for r in results):
        return 0.35, "strong sources"
    if any(r["sources"] for r in results):
        return 0.15, "weak sources"
    return 0.0, "no sources"


def judge_answer(ticket: str, draft: str) -> tuple[float, str]:
    """Raises LLMError so the caller can fall back to the deterministic score alone."""
    data = call_llm_json(JUDGE_SYSTEM, f"Mail: {ticket}\n\nDraft reply:\n{draft}",
                         temperature=0.0)
    try:
        score = max(0.0, min(1.0, float(data.get("score", 0))))
    except (TypeError, ValueError) as exc:
        raise LLMError(f"judge returned a non-numeric score: {exc}") from exc
    return score, str(data.get("note", ""))[:60]
