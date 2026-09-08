"""Account Agent - pulls this customer's real records. The LLM picks which tools to call."""

import time

from agents.account.tools import (find_duplicate_charges, get_customer, get_invoices,
                                  usage_summary)
from llm import LLMError, call_llm_json, warn_fallback
from state import SupportState, dispatch, result
from trace import record, span, step, tag, tools_used

OPTIONAL_TOOLS = ["get_invoices", "usage_summary"]

SYSTEM = """You are the account agent. You already have the customer's profile. Decide which
extra lookups are needed to answer the question you were given.

- get_invoices: payment history, charges, refunds, failed payments
- usage_summary: plan limits, seats, API calls, storage

Reply with JSON only: {"tools": ["get_invoices"], "reason": "<10 words max>"}"""


def account_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    job = dispatch(state, "account")
    query = job.get("query") or state["ticket"]
    email = job.get("details", {}).get("email") or state.get("customer_email", "")

    step("account", f'asked: "{query}"')
    customer = get_customer(email)
    step("account", f"tool get_customer({email}) -> "
                    f"{customer['customer_id'] + ' on ' + customer['plan'] if customer else 'no record'}")
    calls = [record("get_customer", {"email": email},
                    f'{customer["customer_id"]} {customer["plan"]}' if customer else "no match")]

    if not customer:
        return {
            "results": [result("Account Agent", query, "no customer record found",
                               f"ACCOUNT RECORD\nNo customer record for {email or 'this email'}.",
                               [], False)],
            "tool_calls": tag(calls, "Account Agent"),
            "trace": [span("Account Agent", t0, email or "(no email)",
                           f"tools: {tools_used(calls)} | no customer record found")],
        }

    user = (f"Question: {query}\n"
            f"Customer: {customer['name']}, plan {customer['plan']}, status {customer['status']}")
    try:
        data = call_llm_json(SYSTEM, user, temperature=0.0)
        wanted = [t for t in data.get("tools", []) if t in OPTIONAL_TOOLS]
        if not wanted:
            raise LLMError("no usable tool selection returned")
    except LLMError as exc:
        warn_fallback("Account Agent", exc)
        wanted = OPTIONAL_TOOLS

    lines = [f'ACCOUNT RECORD {customer["customer_id"]} {customer["name"]} '
             f'({customer["company"]})',
             f'Plan {customer["plan"]}, status {customer["status"]}, '
             f'renews {customer["renewal_date"]}, pays by {customer["payment_method"]}']
    sources = [customer["customer_id"]]
    headline = f'{customer["customer_id"]} {customer["plan"]}/{customer["status"]}'

    if "get_invoices" in wanted:
        invoices = get_invoices(customer["customer_id"])
        calls.append(record("get_invoices", {"customer_id": customer["customer_id"]},
                            f"{len(invoices)} invoices"))
        lines.append("Invoices: " + "; ".join(
            f'{i["invoice_id"]} {i["date"]} ${i["amount_usd"]:.2f} {i["status"]} '
            f'({i["description"]})' for i in invoices))
        duplicates = find_duplicate_charges(invoices)
        if duplicates:
            ids = ", ".join(i["invoice_id"] for i in duplicates)
            lines.append(f'DUPLICATE CHARGE: {len(duplicates)} identical paid invoices on '
                         f'{duplicates[0]["date"]} for ${duplicates[0]["amount_usd"]:.2f} '
                         f'({ids}) - this is a real double charge')
            sources += [i["invoice_id"] for i in duplicates]
            headline = "duplicate " + "/".join(i["invoice_id"] for i in duplicates)

    if "usage_summary" in wanted:
        usage = usage_summary(customer["customer_id"])
        calls.append(record("usage_summary", {"customer_id": customer["customer_id"]},
                            f'{usage["api_calls"]}, {usage["storage"]}' if usage else "none"))
        if usage:
            lines.append(f'Usage: seats {usage["seats"]}, API {usage["api_calls"]}, '
                         f'storage {usage["storage"]}')

    return {
        "results": [result("Account Agent", query, headline, "\n".join(lines), sources, True)],
        "tool_calls": tag(calls, "Account Agent"),
        "trace": [span("Account Agent", t0, f"{email} | {query[:60]}",
                       f"tools: {tools_used(calls)} | {headline}")],
    }
