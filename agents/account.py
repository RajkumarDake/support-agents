"""Account Agent - pulls this customer's real records. The LLM picks which tools to call."""

import time

from llm import LLMError, call_llm_json, warn_fallback
from state import SupportState
from tools import record
from tools.accounts import find_duplicate_charges, get_customer, get_invoices, usage_summary
from trace import span

OPTIONAL_TOOLS = ["get_invoices", "usage_summary"]

SYSTEM = """You are the account agent. You already have the customer's profile. Decide which
extra lookups are needed to answer their ticket.

- get_invoices: payment history, charges, refunds, failed payments
- usage_summary: plan limits, seats, API calls, storage

Reply with JSON only: {"tools": ["get_invoices"], "reason": "<10 words max>"}"""


def account_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    email = state.get("customer_email", "")
    ticket = state["ticket"]

    customer = get_customer(email)
    calls = [record("get_customer", {"email": email},
                    f'{customer["customer_id"]} {customer["plan"]}' if customer else "no match")]

    if not customer:
        facts = {"found": False, "email": email,
                 "note": "no customer record matches this email address"}
        return {
            "account_facts": facts,
            "tool_calls": calls,
            "trace": [span("Account Agent", t0, email or "(no email)",
                           "no customer record found")],
        }

    user = (f"Ticket: {ticket}\n"
            f"Customer: {customer['name']}, plan {customer['plan']}, status {customer['status']}")
    try:
        data = call_llm_json(SYSTEM, user, temperature=0.0)
        wanted = [t for t in data.get("tools", []) if t in OPTIONAL_TOOLS]
        if not wanted:
            raise LLMError("no usable tool selection returned")
    except LLMError as exc:
        warn_fallback("Account Agent", exc)
        wanted = OPTIONAL_TOOLS

    facts = {"found": True, **customer}

    if "get_invoices" in wanted:
        invoices = get_invoices(customer["customer_id"])
        facts["invoices"] = invoices
        calls.append(record("get_invoices", {"customer_id": customer["customer_id"]},
                            f"{len(invoices)} invoices"))
        duplicates = find_duplicate_charges(invoices)
        if duplicates:
            facts["duplicate_charge"] = duplicates
            facts["duplicate_note"] = (
                f'{len(duplicates)} identical paid invoices on {duplicates[0]["date"]} '
                f'for ${duplicates[0]["amount_usd"]:.2f} - this is a real double charge')

    if "usage_summary" in wanted:
        usage = usage_summary(customer["customer_id"])
        facts["usage"] = usage
        calls.append(record("usage_summary", {"customer_id": customer["customer_id"]},
                            f'{usage["api_calls"]}, {usage["storage"]}' if usage else "none"))

    output = f'{customer["customer_id"]} {customer["plan"]}/{customer["status"]}, ' \
             f'tools: {", ".join(c["tool"] for c in calls)}'
    if facts.get("duplicate_charge"):
        output += " | DUPLICATE CHARGE FOUND"

    return {
        "account_facts": facts,
        "tool_calls": calls,
        "trace": [span("Account Agent", t0, f"{email} | {ticket[:60]}", output)],
    }
