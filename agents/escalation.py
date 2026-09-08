"""Escalation Agent - writes the human handoff and puts the ticket on the queue."""

import time

from agents.evaluator import CONFIDENCE_THRESHOLD
from llm import LLMError, call_llm, warn_fallback
from state import SupportState
from tools import record
from tools.handoff import create_handoff, notify_team
from trace import span

SYSTEM = """You write the handoff note a support agent reads before picking up a ticket.

Exactly three short sections, no preamble:
WHAT THE CUSTOMER WANTS: one line.
WHAT WE ALREADY KNOW: the concrete records and docs found, with their ids.
WHAT THE HUMAN MUST DECIDE: the judgement call the automation cannot make.

Use only the supplied facts. Under 120 words."""


def escalation_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    priority = _priority(state)
    reason = _reason(state)

    facts = _facts_block(state)
    try:
        summary = call_llm(SYSTEM,
                           f"Ticket: {state['ticket']}\nEscalation reason: {reason}\n\n{facts}",
                           temperature=0.0)
    except LLMError as exc:
        warn_fallback("Escalation Agent", exc)
        summary = (f"WHAT THE CUSTOMER WANTS: {state['ticket'][:160]}\n"
                   f"WHAT WE ALREADY KNOW:\n{facts}\n"
                   f"WHAT THE HUMAN MUST DECIDE: {reason}")

    entry = create_handoff(
        priority=priority,
        summary=summary,
        ticket_id=state.get("ticket_id", ""),
        ticket=state["ticket"],
        email=state.get("customer_email", ""),
        category=state.get("category", ""),
        confidence=state.get("confidence", 0.0),
    )
    page = notify_team(priority, state.get("ticket_id", ""))

    calls = [
        record("create_handoff", {"priority": priority, "summary_chars": len(summary)},
               f'queued, sla {entry["sla_hours"]}h'),
        record("notify_team", {"priority": priority}, page["channel"]),
    ]

    return {
        "escalated": True,
        "handoff": entry,
        "tool_calls": calls,
        "trace": [span("Escalation Agent", t0, reason,
                       f"priority={priority} -> human queue (sla {entry['sla_hours']}h)")],
    }


def _priority(state: SupportState) -> str:
    if state.get("priority") == "high" and state.get("sentiment") == "angry":
        return "urgent"
    if state.get("priority") == "high" or state.get("category") == "refund":
        return "high"
    if state.get("confidence", 0) < CONFIDENCE_THRESHOLD:
        return "medium"
    return "low"


def _reason(state: SupportState) -> str:
    reasons = []
    if state.get("confidence", 0) < CONFIDENCE_THRESHOLD:
        reasons.append(f'low confidence {state.get("confidence", 0):.2f}')
    if state.get("category") == "refund":
        reasons.append("refund requests are decided by a human")
    if state.get("sentiment") == "angry":
        reasons.append("customer is angry")
    if state.get("priority") == "high":
        reasons.append("high-priority keywords in the ticket")
    return "; ".join(reasons) or "policy escalation"


def _facts_block(state: SupportState) -> str:
    parts = []
    facts = state.get("account_facts") or {}
    if facts.get("found"):
        parts.append(f'- Account {facts["customer_id"]} ({facts["company"]}), plan '
                     f'{facts["plan"]}, status {facts["status"]}')
        if facts.get("duplicate_note"):
            ids = ", ".join(i["invoice_id"] for i in facts["duplicate_charge"])
            parts.append(f'- {facts["duplicate_note"]} (invoices {ids})')
        elif facts.get("invoices"):
            recent = facts["invoices"][0]
            parts.append(f'- Latest invoice {recent["invoice_id"]} {recent["date"]} '
                         f'${recent["amount_usd"]:.2f} {recent["status"]}')
        if facts.get("usage"):
            parts.append(f'- Usage: {facts["usage"]["api_calls"]}, {facts["usage"]["storage"]}')
    elif facts:
        parts.append("- No customer record matched the email on the ticket")

    diagnosis = state.get("diagnosis") or {}
    if diagnosis.get("error_code"):
        parts.append(f'- Error {diagnosis["error_code"]}: {diagnosis["error"]["title"]}'
                     if diagnosis.get("error") else f'- Error code {diagnosis["error_code"]}')
    for inc in diagnosis.get("incidents", []):
        parts.append(f'- Open incident {inc["id"]}: {inc["title"]} ({inc["status"]})')

    for doc in state.get("docs") or []:
        parts.append(f'- Help doc {doc["id"]}: {doc["title"]}')

    parts.append(f'- Draft the automation produced ({len(state.get("draft", ""))} chars) was '
                 f'scored {state.get("confidence", 0):.2f}')
    return "\n".join(parts)
