"""The graph: the router fans out to the agents a mail needs, the response agent merges them."""

import random
import time

from langgraph.graph import END, StateGraph

from agents.account.agent import account_agent
from agents.escalation.agent import escalation_agent
from agents.knowledge.agent import knowledge_agent
from agents.response.agent import response_agent
from agents.router.agent import router_agent
from agents.troubleshoot.agent import troubleshoot_agent
from state import AGENTS, SupportState, new_state
from trace import save_trace

NODES = {
    "knowledge": knowledge_agent,
    "account": account_agent,
    "troubleshoot": troubleshoot_agent,
    "escalation": escalation_agent,
}


def fan_out(state: SupportState) -> list[str]:
    """Every agent the router dispatched runs in the same superstep."""
    return [d["agent"] for d in state["dispatches"]] or ["knowledge"]


def respond(state: SupportState) -> dict:
    return {"answer": state.get("draft", "")}


def build_graph():
    g = StateGraph(SupportState)
    g.add_node("router", router_agent)
    for name in AGENTS:
        g.add_node(name, NODES[name])
    g.add_node("response", response_agent)
    g.add_node("respond", respond)

    g.set_entry_point("router")
    g.add_conditional_edges("router", fan_out, AGENTS)
    for name in AGENTS:
        g.add_edge(name, "response")
    g.add_edge("response", "respond")
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
