"""The LangGraph state machine that wires the six agents together."""

import random
import re
import time

from langgraph.graph import END, StateGraph

from agents.account import account_agent
from agents.escalation import escalation_agent
from agents.evaluator import evaluator, route_after_eval
from agents.knowledge import knowledge_agent
from agents.response import response_agent
from agents.router import router_agent
from agents.troubleshoot import troubleshoot_agent
from state import SupportState, new_state
from trace import save_trace

ACCOUNT_CATEGORIES = {"billing", "account", "refund"}


def ingest(state: SupportState) -> dict:
    ticket = re.sub(r"\s+", " ", state.get("ticket", "")).strip()
    if not ticket:
        raise ValueError("empty ticket: POST /ticket needs a non-empty 'text' field")
    return {"ticket": ticket, "ticket_id": state.get("ticket_id") or new_ticket_id()}


def route_after_router(state: SupportState) -> str:
    """First conditional edge: which specialist gets the ticket."""
    if state["category"] == "technical":
        return "troubleshoot"
    if (state["category"] in ACCOUNT_CATEGORIES
            and state.get("needs_account_data")
            and state.get("customer_email")):
        return "account"
    return "knowledge"


def respond(state: SupportState) -> dict:
    """Terminal node: the draft becomes the answer the customer sees."""
    answer = state.get("draft", "")
    if state.get("escalated"):
        answer += ("\n\n---\nThis ticket has been passed to a support specialist "
                   f'(priority: {state.get("handoff", {}).get("priority", "medium")}). '
                   "They will follow up directly.")
    return {"answer": answer}


def build_graph():
    g = StateGraph(SupportState)
    g.add_node("ingest", ingest)
    g.add_node("router", router_agent)
    g.add_node("account", account_agent)
    g.add_node("troubleshoot", troubleshoot_agent)
    g.add_node("knowledge", knowledge_agent)
    g.add_node("response", response_agent)
    g.add_node("evaluator", evaluator)
    g.add_node("escalation", escalation_agent)
    g.add_node("respond", respond)

    g.set_entry_point("ingest")
    g.add_edge("ingest", "router")
    g.add_conditional_edges("router", route_after_router,
                            {"account": "account", "troubleshoot": "troubleshoot",
                             "knowledge": "knowledge"})
    # both specialists chain into retrieval, so the writer always has docs to cite
    g.add_edge("account", "knowledge")
    g.add_edge("troubleshoot", "knowledge")
    g.add_edge("knowledge", "response")
    g.add_edge("response", "evaluator")
    g.add_conditional_edges("evaluator", route_after_eval,
                            {"escalate": "escalation", "respond": "respond"})
    g.add_edge("escalation", "respond")
    g.add_edge("respond", END)
    return g.compile()


APP = build_graph()


def new_ticket_id() -> str:
    return str(random.randint(1000, 9999))


def run_ticket(ticket: str, email: str = "", ticket_id: str = "") -> dict:
    """Run one ticket through the graph and persist its trace."""
    t0 = time.perf_counter()
    result = dict(APP.invoke(new_state(ticket, email, ticket_id)))
    result["latency_ms"] = int((time.perf_counter() - t0) * 1000)
    result["agents_used"] = [s["agent"] for s in result.get("trace", [])]
    save_trace(result)
    return result
