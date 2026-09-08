"""Knowledge Agent - BM25 retrieval over the help corpus, with one reformulation retry."""

import re
import time

from agents.knowledge.tools import filter_by_category, search_docs
from llm import LLMError, call_llm, warn_fallback
from state import SupportState, dispatch, result
from trace import record, span, tools_used

# below this BM25 score the top hit is noise, so the agent rewrites the query and retries
WEAK_SCORE = 3.0
STRONG_SCORE = 4.0

SYSTEM = """You turn a vague support question into a short search query for a help-centre index.
Reply with 3-8 keywords only. No punctuation, no explanation, no quotes."""

CATEGORY_TO_DOCS = {"billing": "billing", "refund": "refunds", "technical": "technical",
                    "account": "account"}


def knowledge_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    query = dispatch(state, "knowledge").get("query") or state["ticket"]
    doc_category = CATEGORY_TO_DOCS.get(state.get("category", ""))

    calls = []
    if doc_category:
        in_category = filter_by_category(doc_category)
        calls.append(record("filter_by_category", {"cat": doc_category},
                            f"{len(in_category)} docs in scope"))

    hits = search_docs(query, k=3, category=doc_category)
    calls.append(record("search_docs", {"query": query[:60], "k": 3, "category": doc_category},
                        f"{len(hits)} hits, top={hits[0]['score'] if hits else 0}"))

    if not hits or hits[0]["score"] < WEAK_SCORE:
        # weak retrieval: ask the LLM for better search terms and try once more
        try:
            rewritten = call_llm(SYSTEM, f"Question: {query}", temperature=0.0)[:120]
        except LLMError as exc:
            warn_fallback("Knowledge Agent", exc)
            rewritten = " ".join(w for w in query.split() if len(w) > 3)[:120]
        retry = search_docs(rewritten, k=3)
        calls.append(record("search_docs", {"query": rewritten, "k": 3},
                            f"retry after weak match, {len(retry)} hits"))
        hits = _merge(hits, retry)
    elif doc_category:
        hits = _merge(hits, search_docs(query, k=2))

    hits = sorted(hits, key=lambda d: d["score"], reverse=True)[:3]
    ids = [d["id"] for d in hits]
    strong = bool(hits) and hits[0]["score"] >= STRONG_SCORE and _shares_a_word(query, hits[0])

    context = "\n\n".join(f"HELP DOC {d['id']} - {d['title']}\n{d['excerpt']}" for d in hits)
    headline = f'{len(hits)} docs: {", ".join(ids) or "nothing matched"}'

    return {
        "results": [result("Knowledge Agent", query, headline,
                           context or "No help doc matched this question.", ids, strong)],
        "tool_calls": calls,
        "trace": [span("Knowledge Agent", t0, query,
                       f"tools: {tools_used(calls)} | {headline}")],
    }


def _merge(a: list[dict], b: list[dict]) -> list[dict]:
    seen = {d["id"]: d for d in a}
    for d in b:
        seen.setdefault(d["id"], d)
    return list(seen.values())


def _shares_a_word(query: str, doc: dict) -> bool:
    """A high BM25 score on a doc with no word in common with the query is still noise."""
    words = set(re.findall(r"[a-z]{4,}", query.lower()))
    return bool(words & set(re.findall(r"[a-z]{4,}", (doc["id"] + " " + doc["title"]).lower())))
