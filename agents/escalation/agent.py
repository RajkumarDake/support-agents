"""Escalation Agent - writes the human handoff and puts the ticket on the queue."""

import time

from agents.escalation.tools import create_handoff, notify_team
from llm import LLMError, call_llm, warn_fallback
from state import SupportState, dispatch, result
from trace import record, span, step, tag

SYSTEM = """You write the handoff note a support agent reads before picking up a ticket.

Exactly three short sections, no preamble:
WHAT THE CUSTOMER WANTS: one line per problem in the mail.
WHY IT NEEDS A HUMAN: the policy or judgement call the automation cannot make.
WHAT THE HUMAN MUST DECIDE: the single decision to make.

Use only the supplied facts. Under 120 words."""


def escalation_agent(state: SupportState) -> dict:
    t0 = time.perf_counter()
    query = dispatch(state, "escalation").get("query") or state["ticket"]
    priority = _priority(state)
    reason = _reason(state)
    step("escalation", f"needed because {reason} -> priority {priority}")

    try:
        summary = call_llm(SYSTEM, f"Mail: {state['ticket']}\nReason: {reason}", temperature=0.0)
    except LLMError as exc:
        warn_fallback("Escalation Agent", exc)
        summary = (f"WHAT THE CUSTOMER WANTS: {state['ticket'][:160]}\n"
                   f"WHY IT NEEDS A HUMAN: {reason}\n"
                   f"WHAT THE HUMAN MUST DECIDE: how to resolve it")

    entry = create_handoff(
        priority=priority,
        summary=summary,
        ticket_id=state.get("ticket_id", ""),
        ticket=state["ticket"],
        email=state.get("customer_email", ""),
        category=state.get("category", ""),
    )
    step("escalation", f"tool create_handoff -> queued, first response within {entry['sla_hours']}h")
    page = notify_team(priority, state.get("ticket_id", ""))
    step("escalation", f"tool notify_team -> paged {page['channel']}")

    calls = [
        record("create_handoff", {"priority": priority}, f'queued, sla {entry["sla_hours"]}h'),
        record("notify_team", {"priority": priority}, page["channel"]),
    ]
    context = (f"Escalated to a human, priority {priority}, first response within "
               f'{entry["sla_hours"]}h.\n{summary}')

    return {
        "escalated": True,
        "handoff": entry,
        "results": [result("Escalation Agent", query, f"handed to a human ({priority})",
                           context, [f'queue:{entry["priority"]}'], True)],
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
        reasons.append("refunds are decided by a human")
    if state.get("sentiment") == "angry":
        reasons.append("customer is angry")
    if state.get("priority") == "high":
        reasons.append("high-priority wording in the mail")
    return "; ".join(reasons) or "policy escalation"
