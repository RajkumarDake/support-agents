"""Shared graph state. Every node reads and writes this one typed dict."""

import operator
from typing import Annotated, Any, TypedDict


class SupportState(TypedDict, total=False):
    ticket_id: str
    ticket: str
    customer_email: str

    # router output
    category: str
    route_reason: str
    sentiment: str
    priority: str
    needs_account_data: bool

    # specialist agent output
    docs: list[dict[str, Any]]
    account_facts: dict[str, Any]
    diagnosis: dict[str, Any]

    # response + evaluation
    draft: str
    tone_flags: list[str]
    confidence: float
    eval_notes: list[str]

    # escalation
    escalated: bool
    handoff: dict[str, Any]

    answer: str

    # append-only channels: nodes return only their own new entries
    tool_calls: Annotated[list[dict[str, Any]], operator.add]
    trace: Annotated[list[dict[str, Any]], operator.add]


def new_state(ticket: str, email: str = "", ticket_id: str = "") -> SupportState:
    return {
        "ticket_id": ticket_id,
        "ticket": ticket,
        "customer_email": email.strip().lower(),
        "docs": [],
        "account_facts": {},
        "diagnosis": {},
        "tone_flags": [],
        "eval_notes": [],
        "escalated": False,
        "handoff": {},
        "tool_calls": [],
        "trace": [],
    }
