"""The graph: router fans out to specialists, response merges, escalation catches risky tickets."""

import random
import time

from langgraph.graph import END, StateGraph

from agents.account.agent import account_agent
from agents.escalation.agent import escalation_agent
from agents.knowledge.agent import knowledge_agent
from agents.response.agent import response_agent
from agents.router.agent import router_agent
from agents.troubleshoot.agent import troubleshoot_agent
from state import SupportState, new_state
from trace import save_trace

SPECIALISTS = ["knowledge", "account", "troubleshoot"]


def fan_out(state: SupportState) -> list[str]:
    """Router picked one or more agents; each one runs in the same superstep."""
    return [d["agent"] for d in state["dispatches"]] or ["knowledge"]


def needs_human(state: SupportState) -> str:
    """Refunds, anger, legal and high-priority tickets go to a human."""
    if state.get("category") == "refund":
        return "escalation"
    if state.get("sentiment") == "angry":
        return "escalation"
    if state.get("priority") == "high":
        return "escalation"
    return "respond"


def respond(state: SupportState) -> dict:
    answer = state.get("draft", "")
    if state.get("escalated"):
        priority = state.get("handoff", {}).get("priority", "medium")
        answer += (f"\n\n---\nThis ticket has been passed to a support specialist "
                   f"(priority: {priority}). They will follow up directly.")
    return {"answer": answer}


def build_graph():
    g = StateGraph(SupportState)
    for name, node in [("router", router_agent), ("knowledge", knowledge_agent),
                       ("account", account_agent), ("troubleshoot", troubleshoot_agent),
                       ("response", response_agent), ("escalation", escalation_agent),
                       ("respond", respond)]:
        g.add_node(name, node)

    g.set_entry_point("router")
    g.add_conditional_edges("router", fan_out, SPECIALISTS)
    for name in SPECIALISTS:
        g.add_edge(name, "response")
    g.add_conditional_edges("response", needs_human, ["escalation", "respond"])
    g.add_edge("escalation", "respond")
    g.add_edge("respond", END)
    return g.compile()


APP = build_graph()


def run_ticket(ticket: str, email: str = "", ticket_id: str = "") -> dict:
    t0 = time.perf_counter()
    ticket = " ".join(ticket.split())
    if not ticket:
        raise ValueError("empty ticket: POST /ticket needs a non-empty 'text' field")

    state = new_state(ticket, email, ticket_id or str(random.randint(1000, 9999)))
    result = dict(APP.invoke(state))
    result["latency_ms"] = int((time.perf_counter() - t0) * 1000)
    result["agents_used"] = [s["agent"] for s in result.get("trace", [])]
    save_trace(result)
    return result
