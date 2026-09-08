"""The LangGraph state machine: router fans out to the specialists, response merges them back."""

import random
import re
import time

from langgraph.graph import END, StateGraph

from agents.account.agent import account_agent
from agents.escalation.agent import escalation_agent
from agents.evaluator.agent import evaluator, route_after_eval
from agents.knowledge.agent import knowledge_agent
from agents.response.agent import response_agent
from agents.router.agent import router_agent
from agents.troubleshoot.agent import troubleshoot_agent
from state import SupportState, new_state
from trace import save_trace

SPECIALISTS = ["knowledge", "account", "troubleshoot"]


def ingest(state: SupportState) -> dict:
    ticket = re.sub(r"\s+", " ", state.get("ticket", "")).strip()
    if not ticket:
        raise ValueError("empty ticket: POST /ticket needs a non-empty 'text' field")
    return {"ticket": ticket, "ticket_id": state.get("ticket_id") or new_ticket_id()}


def fan_out(state: SupportState) -> list[str]:
    """The fan-out edge: every agent the router dispatched runs, in parallel, in one superstep."""
    return [d["agent"] for d in state["dispatches"]] or ["knowledge"]


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
    g.add_node("knowledge", knowledge_agent)
    g.add_node("account", account_agent)
    g.add_node("troubleshoot", troubleshoot_agent)
    g.add_node("response", response_agent)
    g.add_node("evaluator", evaluator)
    g.add_node("escalation", escalation_agent)
    g.add_node("respond", respond)

    g.set_entry_point("ingest")
    g.add_edge("ingest", "router")
    g.add_conditional_edges("router", fan_out, SPECIALISTS)
    for name in SPECIALISTS:
        g.add_edge(name, "response")
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
