"""Troubleshoot Agent - matches the error code and open incidents, then orders the fix steps."""

import time

from llm import LLMError, call_llm, warn_fallback
from state import SupportState
from tools import record
from tools.diagnostics import extract_error_code, known_issues, lookup_error
from trace import span

SYSTEM = """You are the troubleshooting agent. Using ONLY the error record and incident notes
supplied, write the fix steps for the customer, ordered from most to least likely to work.

Rules: 3-5 steps, one line each, imperative, numbered "1." to "5.". Invent nothing. If an open
incident explains the problem, make that the first step."""


def troubleshoot_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    ticket = state["ticket"]

    code = extract_error_code(ticket)
    error = lookup_error(code) if code else None
    calls = [record("lookup_error", {"code": code or "(none found)"},
                    error["title"] if error else "no matching error code")]

    keyword = code or _topic(ticket)
    incidents = known_issues(keyword)
    if not incidents:
        incidents = known_issues()
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
        note = "no error code or incident matched - generic triage steps"
    else:
        try:
            steps = call_llm(SYSTEM, f"Ticket: {ticket}\n\n" + "\n\n".join(context),
                             temperature=0.0)
            note = "steps written from error record"
        except LLMError as exc:
            warn_fallback("Troubleshoot Agent", exc)
            source = error["steps"] if error else [incidents[0]["workaround"]]
            steps = "\n".join(f"{n}. {s}" for n, s in enumerate(source, 1))
            note = "steps taken verbatim from error record (LLM fallback)"

    diagnosis = {
        "error_code": code,
        "error": error,
        "incidents": incidents,
        "steps": steps,
    }
    summary = f'code={code or "none"} incidents={[i["id"] for i in incidents] or "none"} | {note}'

    return {
        "diagnosis": diagnosis,
        "tool_calls": calls,
        "trace": [span("Troubleshoot Agent", t0, ticket, summary)],
    }


TOPICS = ["upload", "webhook", "sso", "mobile", "sync", "export", "login", "billing"]


def _topic(ticket: str) -> str:
    low = ticket.lower()
    return next((t for t in TOPICS if t in low), "")
