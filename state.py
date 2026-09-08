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
    dispatches: list[dict[str, Any]]

    # response + evaluation
    draft: str
    tone_flags: list[str]
    confidence: float
    eval_notes: list[str]

    # escalation
    escalated: bool
    handoff: dict[str, Any]

    answer: str

    # append-only channels: the fanned-out specialists each add their own entries,
    # so parallel writes merge instead of clobbering each other
    results: Annotated[list[dict[str, Any]], operator.add]
    tool_calls: Annotated[list[dict[str, Any]], operator.add]
    trace: Annotated[list[dict[str, Any]], operator.add]


def new_state(ticket: str, email: str = "", ticket_id: str = "") -> SupportState:
    return {
        "ticket_id": ticket_id,
        "ticket": ticket,
        "customer_email": email.strip().lower(),
        "dispatches": [],
        "tone_flags": [],
        "eval_notes": [],
        "escalated": False,
        "handoff": {},
        "results": [],
        "tool_calls": [],
        "trace": [],
    }


def dispatch(state: SupportState, agent: str) -> dict[str, Any]:
    """The router's sub-query for one agent, or {} if that agent was not dispatched."""
    return next((d for d in state.get("dispatches", []) if d["agent"] == agent), {})


def result(agent: str, query: str, headline: str, context: str,
           sources: list[str], strong: bool) -> dict[str, Any]:
    """What every specialist appends to state['results'] for the response agent to merge."""
    return {"agent": agent, "query": query, "headline": headline,
            "context": context, "sources": sources, "strong": strong}
