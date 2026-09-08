"""Router Agent - splits the mail into problems and dispatches a sub-query to each agent."""

import time

from agents.router.tools import check_priority_keywords, detect_sentiment
from llm import LLMError, call_llm_json, warn_fallback
from state import SupportState
from trace import record, span

AGENTS = ["knowledge", "account", "troubleshoot"]
CATEGORIES = ["billing", "technical", "account", "refund", "unclear"]

SYSTEM = """You are the router in a customer support system. One mail often contains several
separate problems. Split it and dispatch each problem to the agent that can solve it.

Agents:
- account: needs THIS customer's records - invoices, charges, plan, seats, usage
- troubleshoot: error codes, failures, crashes, uploads, sync, sign-in problems
- knowledge: how-to, policy and general product questions answered from the help centre

For each problem write a short sub-query in your own words, plus the details that agent needs
(account: {"email": "..."}, troubleshoot: {"error_code": "ERR_1234"}). Dispatch every agent the
mail needs - one, two or three - but at most one dispatch per agent.

Also give the overall category: billing, technical, account, refund or unclear.

Reply with JSON only:
{"category": "...", "reason": "<12 words max>",
 "dispatches": [{"agent": "account", "query": "...", "details": {}}]}"""

# fallback dispatch table, used only when the LLM is unavailable
KEYWORDS = {
    "account": ["charge", "charged", "invoice", "bill", "payment", "refund", "card",
                "seat", "usage", "plan", "proration", "receipt"],
    "troubleshoot": ["err_", "error", "failing", "fails", "failed", "crash", "bug", "upload",
                     "sync", "api", "webhook", "sso", "login", "broken", "timeout"],
    "knowledge": ["how do i", "how can i", "how to", "where do i", "what is", "policy",
                  "team member", "invite", "role", "permission", "password", "2fa"],
}

FALLBACK_CATEGORY = {"troubleshoot": "technical", "account": "billing", "knowledge": "unclear"}


def router_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    ticket = state["ticket"]
    email = state.get("customer_email", "")

    sentiment = detect_sentiment(ticket)
    priority = check_priority_keywords(ticket)
    calls = [
        record("detect_sentiment", {"text": ticket[:80]}, sentiment["sentiment"]),
        record("check_priority_keywords", {"text": ticket[:80]},
               f'{priority["priority"]} {priority["matched"] or "no risk words"}'),
    ]

    user = (f"Mail: {ticket}\n"
            f"Detected sentiment: {sentiment['sentiment']}\n"
            f"Priority keywords: {priority['matched'] or 'none'}\n"
            f"Customer email on file: {email or 'none'}")

    try:
        data = call_llm_json(SYSTEM, user, temperature=0.0)
        category = str(data.get("category", "")).lower().strip()
        if category not in CATEGORIES:
            raise LLMError(f"router returned unknown category {category!r}")
        reason = str(data.get("reason", "")).strip() or "no reason given"
        dispatches = clean_dispatches(data.get("dispatches"), ticket, email)
        if not dispatches:
            raise LLMError("router dispatched no agents")
    except LLMError as exc:
        warn_fallback("Router Agent", exc)
        dispatches = keyword_dispatches(ticket, email)
        category = FALLBACK_CATEGORY[dispatches[0]["agent"]]
        reason = "keyword fallback dispatch"

    # a refund request is always a refund ticket, whatever the model called it
    if priority["refund_intent"] and category in ("billing", "account"):
        category = "refund"
        reason += " (refund wording present)"

    names = ", ".join(d["agent"] for d in dispatches)
    return {
        "category": category,
        "route_reason": reason,
        "sentiment": sentiment["sentiment"],
        "priority": priority["priority"],
        "dispatches": dispatches,
        "tool_calls": calls,
        "trace": [span("Router Agent", t0, ticket,
                       f"dispatched: {names} | category={category} "
                       f"sentiment={sentiment['sentiment']} priority={priority['priority']}")],
    }


def clean_dispatches(raw: object, ticket: str, email: str) -> list[dict]:
    """Keep one valid dispatch per agent. Account is useless without an email, so drop it."""
    out: dict[str, dict] = {}
    for item in raw if isinstance(raw, list) else []:
        if not isinstance(item, dict):
            continue
        agent = str(item.get("agent", "")).lower().strip()
        if agent not in AGENTS or agent in out:
            continue
        if agent == "account" and not email:
            continue
        details = item.get("details") if isinstance(item.get("details"), dict) else {}
        if agent == "account":
            details["email"] = email
        out[agent] = {"agent": agent,
                      "query": str(item.get("query") or ticket)[:200],
                      "details": details}
    return list(out.values())


def keyword_dispatches(ticket: str, email: str) -> list[dict]:
    """Deterministic fan-out used whenever the LLM call fails."""
    low = ticket.lower()
    raw = [{"agent": agent, "query": ticket, "details": {}}
           for agent, words in KEYWORDS.items() if any(w in low for w in words)]
    return clean_dispatches(raw, ticket, email) or [
        {"agent": "knowledge", "query": ticket, "details": {}}]
