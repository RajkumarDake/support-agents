"""Observability: one span per agent, a rich tree in the terminal, JSON on disk."""

import json
import logging
import pathlib
import time
from typing import Any

from rich.console import Console
from rich.text import Text
from rich.tree import Tree

TRACE_DIR = pathlib.Path(__file__).resolve().parent / "traces"
console = Console(width=110)
log = logging.getLogger("support")


def step(agent: str, message: str) -> None:
    """A live line for one decision, so the terminal explains itself as the graph runs."""
    log.info("%-13s %s", agent, message)


def span(agent: str, t0: float, input_summary: str, output_summary: str) -> dict[str, Any]:
    return {
        "agent": agent,
        "latency_ms": int((time.perf_counter() - t0) * 1000),
        "input_summary": input_summary[:160],
        "output_summary": output_summary[:200],
    }


def record(tool: str, args: dict[str, Any], result: str) -> dict[str, Any]:
    """Every tool call an agent makes is recorded in state['tool_calls'] with this shape."""
    return {"tool": tool, "args": args, "result": result}


def tag(calls: list[dict[str, Any]], agent: str) -> list[dict[str, Any]]:
    """Stamp the agent name on its tool calls so the trace shows who called what."""
    for c in calls:
        c["agent"] = agent
    return calls


def tools_used(calls: list[dict[str, Any]]) -> str:
    return ", ".join(dict.fromkeys(c["tool"] for c in calls))


def print_trace(result: dict[str, Any]) -> None:
    ticket = result.get("ticket", "")
    headline = ticket if len(ticket) <= 70 else ticket[:67] + "..."
    label = Text(f"Ticket #{result.get('ticket_id', '?')}  ", style="bold")
    label.append(f'"{headline}"', style="italic cyan")
    tree = Tree(label, guide_style="grey42")

    calls = result.get("tool_calls", [])
    for entry in result.get("trace", []):
        summary = entry["output_summary"]
        if len(summary) > 68:
            summary = summary[:65] + "..."
        line = Text(f"{entry['agent']:<20}", style="bold white")
        line.append(f"{entry['latency_ms']:>6}ms  ", style="yellow")
        line.append(summary, style="grey70")
        node = tree.add(line)

        # the tools this agent called, under the agent that called them
        for c in [c for c in calls if c.get("agent") == entry["agent"]]:
            args = ", ".join(f"{k}={v}" for k, v in c["args"].items())
            leaf = Text(f"{c['tool']}(", style="cyan")
            leaf.append(args[:60], style="grey50")
            leaf.append(") -> ", style="cyan")
            leaf.append(str(c["result"])[:60], style="grey70")
            node.add(leaf)

    console.print(tree)

    total = sum(e["latency_ms"] for e in result.get("trace", []))
    verdict = "ESCALATED" if result.get("escalated") else "ANSWERED"
    style = "bold red" if result.get("escalated") else "bold green"
    summary = Text("   ")
    summary.append(verdict, style=style)
    summary.append(f"  total {total}ms", style="yellow")
    console.print(summary)
    console.print()


def save_trace(result: dict[str, Any]) -> pathlib.Path:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    path = TRACE_DIR / f"{result.get('ticket_id', 'unknown')}.json"
    path.write_text(json.dumps(result, indent=2, default=str) + "\n")
    return path
