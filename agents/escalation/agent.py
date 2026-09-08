"""Escalation Agent - writes the human handoff and puts the ticket on the queue."""

import time

from agents.escalation.tools import create_handoff, notify_team
from llm import LLMError, call_llm, warn_fallback
from state import SupportState
from trace import record, span, tag

SYSTEM = """You write the handoff note a support agent reads before picking up a ticket.

Exactly three short sections, no preamble:
WHAT THE CUSTOMER WANTS: one line per problem in the mail.
WHAT WE ALREADY KNOW: the concrete records and docs found, with their ids.
WHAT THE HUMAN MUST DECIDE: the judgement call the automation cannot make.

Use only the supplied facts. Under 150 words."""


def escalation_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    priority = _priority(state)
    reason = _reason(state)
    facts = _facts_block(state)

    try:
        summary = call_llm(SYSTEM,
                           f"Mail: {state['ticket']}\nEscalation reason: {reason}\n\n{facts}",
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
        "tool_calls": tag(calls, "Escalation Agent"),
        "trace": [span("Escalation Agent", t0, reason,
                       f"priority={priority} -> human queue (sla {entry['sla_hours']}h)")],
    }


def _priority(state: SupportState) -> str:
    if state.get("priority") == "high" and state.get("sentiment") == "angry":
        return "urgent"
    if state.get("priority") == "high" or state.get("category") == "refund":
        return "high"
    return "medium"


def _reason(state: SupportState) -> str:
    reasons = []
    if state.get("category") == "refund":
        reasons.append("refund requests are decided by a human")
    if state.get("sentiment") == "angry":
        reasons.append("customer is angry")
    if state.get("priority") == "high":
        reasons.append("high-priority keywords in the ticket")
    return "; ".join(reasons) or "policy escalation"


def _facts_block(state: SupportState) -> str:
    parts = [f'{r["agent"]} - asked: {r["query"]}\n{r["context"]}'
             for r in state.get("results") or []]
    return "\n\n".join(parts)
