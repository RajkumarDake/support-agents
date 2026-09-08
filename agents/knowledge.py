"""Knowledge Agent - BM25 retrieval over the help corpus, with one reformulation retry."""

import time

from llm import LLMError, call_llm, warn_fallback
from state import SupportState
from tools import record
from tools.docs import filter_by_category, search_docs
from trace import span

# below this BM25 score the top hit is noise, so the agent rewrites the query and retries
WEAK_SCORE = 3.0

SYSTEM = """You turn a vague support ticket into a short search query for a help-centre index.
Reply with 3-8 keywords only. No punctuation, no explanation, no quotes."""

CATEGORY_TO_DOCS = {"billing": "billing", "refund": "refunds", "technical": "technical",
                    "account": "account"}


def knowledge_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    ticket = state["ticket"]
    doc_category = CATEGORY_TO_DOCS.get(state.get("category", ""))

    calls = []
    if doc_category:
        in_category = filter_by_category(doc_category)
        calls.append(record("filter_by_category", {"cat": doc_category},
                            f"{len(in_category)} docs in scope"))

    # rank inside the category, then again across everything, and merge
    hits = search_docs(ticket, k=3, category=doc_category)
    calls.append(record("search_docs", {"query": ticket[:60], "k": 3, "category": doc_category},
                        f"{len(hits)} hits, top={hits[0]['score'] if hits else 0}"))

    reformulated = ""
    if not hits or hits[0]["score"] < WEAK_SCORE:
        # weak retrieval: ask the LLM for better search terms and try once more
        try:
            reformulated = call_llm(SYSTEM, f"Ticket: {ticket}", temperature=0.0)[:120]
        except LLMError as exc:
            warn_fallback("Knowledge Agent", exc)
            reformulated = " ".join(w for w in ticket.split() if len(w) > 3)[:120]
        retry = search_docs(reformulated, k=3, category=None)
        calls.append(record("search_docs", {"query": reformulated, "k": 3},
                            f"retry after weak match, {len(retry)} hits"))
        hits = _merge(hits, retry)

    if doc_category:
        hits = _merge(hits, search_docs(ticket, k=2, category=None))

    hits = sorted(hits, key=lambda d: d["score"], reverse=True)[:3]
    summary = ", ".join(d["id"] for d in hits) or "no docs matched"

    return {
        "docs": hits,
        "tool_calls": calls,
        "trace": [span("Knowledge Agent", t0,
                       reformulated or ticket,
                       f"{len(hits)} docs matched: {summary}")],
    }


def _merge(a: list[dict], b: list[dict]) -> list[dict]:
    seen = {d["id"]: d for d in a}
    for d in b:
        seen.setdefault(d["id"], d)
    return list(seen.values())
