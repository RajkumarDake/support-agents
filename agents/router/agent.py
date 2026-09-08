"""Router Agent - splits the mail into problems and dispatches a sub-query to each agent."""

import time

from agents.router.tools import check_priority_keywords, detect_sentiment
from llm import LLMError, call_llm_json, warn_fallback
from state import AGENTS, CATEGORIES, SupportState
from trace import record, span, step, tag

SYSTEM = """You are the router in a customer support system. One mail often contains several
separate problems. Split it and dispatch each problem to the agent that can solve it.

Agents:
- account: needs THIS customer's records - invoices, charges, plan, seats, usage
- troubleshoot: error codes, failures, crashes, uploads, sync, sign-in problems
- knowledge: how-to, policy and general product questions answered from the help centre
- escalation: a human MUST decide - only for an explicit refund or cancellation request, a legal
  threat, or a genuinely angry customer. Reporting a duplicate charge is NOT escalation: the
  account agent confirms it from the invoices.

Only dispatch account when answering needs THIS customer's records. A general how-to or policy
question is a knowledge job, even when it is about billing or seats.

Do not dispatch escalation for a normal question, a bug, or a charge the customer only wants
explained. When you do dispatch it, the specialists still run - they gather the facts while
escalation writes the handoff.

For each problem write a short sub-query in your own words, plus the details that agent needs
(account: {"email": "..."}, troubleshoot: {"error_code": "ERR_1234"}). Dispatch every agent the
mail needs - one to four - but at most one dispatch per agent.

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

    step("router", f"reading mail from {email or 'unknown sender'}: {ticket[:70]}")

    sentiment = detect_sentiment(ticket)
    priority = check_priority_keywords(ticket)
    step("router", f"tool detect_sentiment -> {sentiment['sentiment']} "
                   f"(matched {sentiment['matched'] or 'nothing'})")
    step("router", f"tool check_priority_keywords -> {priority['priority']} "
                   f"(matched {priority['matched'] or 'nothing'})")
    calls = [
        record("detect_sentiment", {"text": ticket[:80]}, sentiment["sentiment"]),
        record("check_priority_keywords", {"text": ticket[:80]},
               f'{priority["priority"]} {priority["matched"] or "no risk words"}'),
    ]

    user = (f"Mail: {ticket}\n"
            f"Detected sentiment: {sentiment['sentiment']}\n"
            f"Priority keywords: {priority['matched'] or 'none'}\n"
            f"Customer email on file: {email or 'none'}")

    step("router", "asking the LLM to split the mail into problems")
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
        step("router", "LLM unavailable, using the keyword fallback table")

    # a refund request is always a refund ticket, whatever the model called it
    if priority["refund_intent"] and category in ("billing", "account"):
        step("router", f"refund wording found, overriding category {category} -> refund")
        category = "refund"
        reason += " (refund wording present)"

    # risk always reaches a human, even if the model missed it
    if _needs_human(category, sentiment, priority) and \
            not any(d["agent"] == "escalation" for d in dispatches):
        step("router", f"risk check: category={category} sentiment={sentiment['sentiment']} "
                       f"priority={priority['priority']} -> adding escalation")
        dispatches.append({"agent": "escalation", "query": ticket, "details": {}})

    if not _needs_human(category, sentiment, priority):
        step("router", "risk check: nothing needs a human, answering automatically")

    step("router", f"category={category} because {reason}")
    for d in dispatches:
        step("router", f'-> {d["agent"]}: "{d["query"]}" details={d["details"] or "{}"}')
    step("router", f"dispatching {len(dispatches)} agents in parallel")

    names = ", ".join(d["agent"] for d in dispatches)
    return {
        "category": category,
        "route_reason": reason,
        "sentiment": sentiment["sentiment"],
        "priority": priority["priority"],
        "dispatches": dispatches,
        "tool_calls": tag(calls, "Router Agent"),
        "trace": [span("Router Agent", t0, ticket,
                       f"dispatched: {names} | category={category} "
                       f"sentiment={sentiment['sentiment']} priority={priority['priority']}")],
    }


def _needs_human(category: str, sentiment: dict, priority: dict) -> bool:
    """A human is needed for money decisions, legal threats and angry customers - nothing else.

    Reporting a duplicate charge is not one of these: the account agent can confirm it from the
    invoices and explain it. Only an actual refund or cancellation request is a human decision.
    """
    return (priority["refund_intent"]
            or "legal" in priority["kinds"]
            or sentiment["sentiment"] == "angry")


def collect(state: SupportState) -> dict:
    """Agents report back here. The router gathers their findings, then hands them to response."""
    t0 = time.perf_counter()
    results = state.get("results") or []
    names = ", ".join(r["agent"].split()[0].lower() for r in results)
    step("router", f"all {len(results)} agents reported back")
    for r in results:
        step("router", f"<- {r['agent']}: {r['headline']} (sources: {', '.join(r['sources']) or 'none'})")
    step("router", "handing every finding to the response agent")
    return {
        "trace": [span("Router Agent (collect)", t0, f"{len(results)} agents reported",
                       f"collected findings from {names or 'no agent'}")],
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
