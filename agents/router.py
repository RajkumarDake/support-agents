"""Router Agent - classifies the ticket and decides which specialist runs next."""

import time

from llm import LLMError, call_llm_json, warn_fallback
from state import SupportState
from tools import record
from tools.sentiment import check_priority_keywords, detect_sentiment
from trace import span

CATEGORIES = ["billing", "technical", "account", "refund", "unclear"]

SYSTEM = """You are the routing agent in a customer support system. You classify one ticket.

Categories:
- billing: charges, invoices, payment methods, proration, billing cycles
- technical: errors, error codes, uploads, API, integrations, sync, sign-in failures
- account: team members, roles, permissions, plan details, usage, workspace settings
- refund: the customer explicitly wants money back or is cancelling and wants a credit
- unclear: too vague to route confidently

Also decide `needs_account_data`: true only if answering requires looking up THIS customer's
records (their invoices, their plan, their usage). A general how-to question does not.

Reply with JSON only:
{"category": "...", "reason": "<12 words max>", "needs_account_data": true|false}"""

HOWTO_HINTS = ("how do i", "how can i", "how to", "where do i", "what is the", "can i ")

KEYWORD_MAP = [
    ("refund", ["refund", "money back", "chargeback", "reimburse"]),
    ("billing", ["charge", "charged", "invoice", "bill", "payment", "card", "declined",
                 "proration", "vat", "receipt"]),
    ("technical", ["err_", "error", "failing", "fails", "failed", "crash", "bug", "upload",
                   "sync", "api", "webhook", "sso", "login", "broken", "timeout"]),
    ("account", ["team member", "teammate", "invite", "seat", "role", "permission", "password",
                 "plan", "usage", "workspace", "owner", "admin", "2fa"]),
]


def keyword_route(ticket: str) -> tuple[str, str, bool]:
    """Deterministic fallback used whenever the LLM call fails."""
    low = ticket.lower()
    for category, words in KEYWORD_MAP:
        hit = next((w for w in words if w in low), None)
        if hit:
            needs = category in ("billing", "refund", "account") and not any(
                h in low for h in HOWTO_HINTS)
            return category, f"keyword fallback matched '{hit}'", needs
    return "unclear", "keyword fallback found nothing specific", False


def router_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    ticket = state["ticket"]

    sentiment = detect_sentiment(ticket)
    priority = check_priority_keywords(ticket)
    calls = [
        record("detect_sentiment", {"text": ticket[:80]}, sentiment["sentiment"]),
        record("check_priority_keywords", {"text": ticket[:80]},
               f'{priority["priority"]} {priority["matched"] or "no risk words"}'),
    ]

    user = (f"Ticket: {ticket}\n"
            f"Detected sentiment: {sentiment['sentiment']}\n"
            f"Priority keywords: {priority['matched'] or 'none'}\n"
            f"Customer email on file: {state.get('customer_email') or 'none'}")

    try:
        data = call_llm_json(SYSTEM, user, temperature=0.0)
        category = str(data.get("category", "")).lower().strip()
        if category not in CATEGORIES:
            raise LLMError(f"router returned unknown category {category!r}")
        reason = str(data.get("reason", "")).strip() or "no reason given"
        needs_account = bool(data.get("needs_account_data"))
    except LLMError as exc:
        warn_fallback("Router Agent", exc)
        category, reason, needs_account = keyword_route(ticket)

    # a refund request is always a refund ticket, whatever the model called it
    if priority["refund_intent"] and category == "billing":
        category = "refund"
        reason += " (refund wording present)"

    return {
        "category": category,
        "route_reason": reason,
        "sentiment": sentiment["sentiment"],
        "priority": priority["priority"],
        "needs_account_data": needs_account,
        "tool_calls": calls,
        "trace": [span("Router Agent", t0, ticket,
                       f"category={category} sentiment={sentiment['sentiment']} "
                       f"priority={priority['priority']}")],
    }
