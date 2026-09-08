"""Response Agent - writes the customer-facing reply from what earlier agents put in state."""

import json
import time

from llm import LLMError, call_llm, warn_fallback
from state import SupportState
from tools import record
from tools.writing import check_tone, get_template
from trace import span

SYSTEM = """You are the response agent for a customer support team. Write the reply that is
sent to the customer.

Hard rules:
- Use ONLY the facts in the CONTEXT block. Never invent invoice IDs, dates, amounts or policy.
- If the context does not answer the question, say what you can confirm and what you need
  from the customer. Do not guess.
- Open with a greeting, no more than 200 words, plain sentences, no marketing tone.
- Do not promise a refund or a deadline. A human decides those.
- End with a line "Sources: <ids>" listing the doc ids or record ids you actually used."""


def response_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    category = state.get("category", "unclear")

    template = get_template(category)
    calls = [record("get_template", {"category": category}, f"{len(template)} char template")]

    context, sources = _build_context(state)
    user = (f"CONTEXT\n{context}\n\nCUSTOMER TICKET\n{state['ticket']}\n\n"
            f"Reply in the shape of this template (adapt the wording):\n{template}")

    try:
        draft = call_llm(SYSTEM, user, temperature=0.3)
    except LLMError as exc:
        warn_fallback("Response Agent", exc)
        draft = _template_reply(state, template, context, sources)

    flags = check_tone(draft)
    calls.append(record("check_tone", {"draft_chars": len(draft)},
                        ", ".join(flags) if flags else "clean"))

    # one repair pass when the tone checker objects
    if flags:
        try:
            draft = call_llm(SYSTEM,
                             f"Rewrite this reply to fix: {', '.join(flags)}.\n\n{draft}",
                             temperature=0.3)
            flags = check_tone(draft)
            calls.append(record("check_tone", {"pass": 2},
                                ", ".join(flags) if flags else "clean after rewrite"))
        except LLMError as exc:
            warn_fallback("Response Agent (tone repair)", exc)

    return {
        "draft": draft,
        "tone_flags": flags,
        "tool_calls": calls,
        "trace": [span("Response Agent", t0, f"sources: {', '.join(sources) or 'none'}",
                       f"draft {len(draft)} chars, tone {'clean' if not flags else flags}")],
    }


def _build_context(state: SupportState) -> tuple[str, list[str]]:
    """Everything the writer is allowed to use, plus the source ids to cite."""
    parts, sources = [], []

    facts = state.get("account_facts") or {}
    if facts.get("found"):
        sources.append(facts["customer_id"])
        parts.append("ACCOUNT RECORD\n" + json.dumps(
            {k: v for k, v in facts.items() if k != "found"}, indent=2, default=str))
    elif facts:
        parts.append(f"ACCOUNT RECORD\nNo customer record for {facts.get('email') or 'this email'}.")

    diagnosis = state.get("diagnosis") or {}
    if diagnosis.get("steps"):
        if diagnosis.get("error_code"):
            sources.append(diagnosis["error_code"])
        sources += [i["id"] for i in diagnosis.get("incidents", [])]
        parts.append("DIAGNOSIS\n" + diagnosis["steps"])
        for inc in diagnosis.get("incidents", []):
            parts.append(f"OPEN INCIDENT {inc['id']}: {inc['summary']} "
                         f"Workaround: {inc['workaround']}")

    for doc in state.get("docs") or []:
        sources.append(doc["id"])
        parts.append(f"HELP DOC {doc['id']} - {doc['title']}\n{doc['excerpt']}")

    return "\n\n".join(parts) or "No supporting facts were retrieved.", sources


def _template_reply(state: SupportState, template: str, context: str,
                    sources: list[str]) -> str:
    """Deterministic reply used when the LLM is unavailable."""
    facts = state.get("account_facts") or {}
    name = f' {facts["name"].split()[0]}' if facts.get("name") else ""

    lines = []
    if facts.get("duplicate_note"):
        lines.append(f'- {facts["duplicate_note"]}')
    if facts.get("usage"):
        lines.append(f'- Plan {facts["usage"]["plan"]}, seats {facts["usage"]["seats"]}, '
                     f'API {facts["usage"]["api_calls"]}, storage {facts["usage"]["storage"]}')
    diagnosis = state.get("diagnosis") or {}
    if diagnosis.get("steps"):
        lines.append(diagnosis["steps"])
    for doc in (state.get("docs") or [])[:2]:
        lines.append(f'- {doc["title"]}: {doc["excerpt"][:200]}')

    body = "\n".join(lines) or "- I could not find a confirmed answer for this yet."
    next_step = ("A member of the support team is picking this up and will reply with a decision."
                 if state.get("category") == "refund"
                 else "Let me know if that does not cover it and I will dig further.")
    reply = template.format(name=name, facts=body, next_step=next_step)
    return reply + f"\n\nSources: {', '.join(sources) or 'none'}"
