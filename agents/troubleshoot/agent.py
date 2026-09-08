"""Troubleshoot Agent - matches the error code and open incidents, then orders the fix steps."""

import time

from agents.troubleshoot.tools import extract_error_code, known_issues, lookup_error
from llm import LLMError, call_llm, warn_fallback
from state import SupportState, dispatch, result
from trace import record, span, tools_used

SYSTEM = """You are the troubleshooting agent. Using ONLY the error record and incident notes
supplied, write the fix steps for the customer, ordered from most to least likely to work.

Rules: 3-5 steps, one line each, imperative, numbered "1." to "5.". Invent nothing. If an open
incident explains the problem, make that the first step."""

TOPICS = ["upload", "webhook", "sso", "mobile", "sync", "export", "login", "billing"]


def troubleshoot_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    job = dispatch(state, "troubleshoot")
    query = job.get("query") or state["ticket"]
    code = job.get("details", {}).get("error_code") or extract_error_code(query) \
        or extract_error_code(state["ticket"])

    error = lookup_error(code) if code else None
    calls = [record("lookup_error", {"code": code or "(none found)"},
                    error["title"] if error else "no matching error code")]

    keyword = code if error else _topic(query)
    # an unfiltered incident list is context, not evidence, so it does not count as a match
    matched = known_issues(keyword) if keyword else []
    incidents = matched or known_issues()
    calls.append(record("known_issues", {"keyword": keyword},
                        ", ".join(i["id"] for i in incidents) or "no open incidents"))

    context = []
    if error:
        context.append(f"Error {code}: {error['title']}\nCause: {error['cause']}\n"
                       "Documented steps:\n" + "\n".join(f"- {s}" for s in error["steps"]))
    for inc in incidents:
        context.append(f"Open incident {inc['id']}: {inc['title']} ({inc['status']})\n"
                       f"{inc['summary']}\nWorkaround: {inc['workaround']}")

    if not context:
        steps = ("1. Reproduce the problem and note the exact time and any error code shown.\n"
                 "2. Retry in an incognito window with extensions disabled.\n"
                 "3. Send support the error code, timestamp and a screenshot.")
    else:
        try:
            steps = call_llm(SYSTEM, f"Problem: {query}\n\n" + "\n\n".join(context),
                             temperature=0.0)
        except LLMError as exc:
            warn_fallback("Troubleshoot Agent", exc)
            source = error["steps"] if error else [incidents[0]["workaround"]]
            steps = "\n".join(f"{n}. {s}" for n, s in enumerate(source, 1))

    sources = ([code] if error else []) + [i["id"] for i in incidents]
    headline = " + ".join(sources) or "no error code or incident matched"

    return {
        "results": [result("Troubleshoot Agent", query, headline,
                           "DIAGNOSIS\n" + steps + "\n\n" + "\n\n".join(context),
                           sources, bool(error or matched))],
        "tool_calls": calls,
        "trace": [span("Troubleshoot Agent", t0, query,
                       f"tools: {tools_used(calls)} | {headline}")],
    }


def _topic(text: str) -> str:
    low = text.lower()
    return next((t for t in TOPICS if t in low), "")
