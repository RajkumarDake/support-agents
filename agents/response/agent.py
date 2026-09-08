"""Response Agent - merges every agent result in state into one reply to the customer."""

import time

from agents.response.tools import check_tone, get_template
from llm import LLMError, call_llm, warn_fallback
from state import SupportState
from trace import record, span, tag

SYSTEM = """You are the response agent for a customer support team. Write the reply that is
sent to the customer.

Hard rules:
- The mail may contain several separate problems. Answer EVERY one, each in its own short
  paragraph, in the order listed.
- Use ONLY the facts in the CONTEXT block. Never invent invoice IDs, dates, amounts or policy.
- If the context does not answer a problem, say what you can confirm and what you need from the
  customer. Do not guess.
- Open with a greeting, no more than 250 words, plain sentences, no marketing tone.
- Do not promise a refund or a deadline. A human decides those.
- End with a line "Sources: <ids>" listing the doc ids or record ids you actually used."""


def response_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    results = state.get("results") or []
    category = state.get("category", "unclear")

    template = get_template(category)
    calls = [record("get_template", {"category": category}, f"{len(template)} char template")]

    problems = "\n".join(f"{n}. {r['query']}" for n, r in enumerate(results, 1))
    context = "\n\n".join(f"--- {r['agent']} was asked: {r['query']}\n{r['context']}"
                          for r in results)
    sources = [s for r in results for s in r["sources"]]

    user = (f"CONTEXT\n{context or 'No supporting facts were retrieved.'}\n\n"
            f"CUSTOMER MAIL\n{state['ticket']}\n\n"
            f"PROBLEMS TO ANSWER\n{problems}\n\n"
            f"Reply in the shape of this template (adapt the wording):\n{template}")

    try:
        draft = call_llm(SYSTEM, user, temperature=0.3)
    except LLMError as exc:
        warn_fallback("Response Agent", exc)
        draft = _template_reply(state, template, results, sources)

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

    merged = ", ".join(r["agent"].split()[0].lower() for r in results)
    return {
        "draft": draft,
        "tone_flags": flags,
        "tool_calls": tag(calls, "Response Agent"),
        "trace": [span("Response Agent", t0, f"sources: {', '.join(sources) or 'none'}",
                       f"merged {len(results)} agent results ({merged}), "
                       f"draft {len(draft)} chars, tone {'clean' if not flags else flags}")],
    }


def _template_reply(state: SupportState, template: str, results: list[dict],
                    sources: list[str]) -> str:
    """Deterministic reply used when the LLM is unavailable: one block per agent result."""
    blocks = [f'{r["query"]}\n{r["context"][:600]}' for r in results]
    body = "\n\n".join(blocks) or "- I could not find a confirmed answer for this yet."
    next_step = ("A member of the support team is picking this up and will reply with a decision."
                 if state.get("category") == "refund"
                 else "Let me know if that does not cover it and I will dig further.")
    reply = template.format(name="", facts=body, next_step=next_step)
    return reply + f"\n\nSources: {', '.join(sources) or 'none'}"
