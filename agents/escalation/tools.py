"""Escalation Agent tools: write to the human queue and page the on-call team."""

import json
import pathlib
import sys
from datetime import datetime, timezone

QUEUE_PATH = pathlib.Path(__file__).resolve().parents[2] / "data" / "human_queue.json"

SLA_HOURS = {"urgent": 1, "high": 4, "medium": 24, "low": 72}


def read_queue() -> list[dict]:
    if not QUEUE_PATH.exists():
        return []
    text = QUEUE_PATH.read_text().strip()
    return json.loads(text) if text else []


def create_handoff(priority: str, summary: str, ticket_id: str = "",
                   ticket: str = "", email: str = "", category: str = "") -> dict:
    """Appends a handoff record to data/human_queue.json and returns it."""
    entry = {
        "ticket_id": ticket_id,
        "priority": priority,
        "sla_hours": SLA_HOURS.get(priority, 24),
        "category": category,
        "customer_email": email,
        "ticket": ticket,
        "summary": summary,
        "status": "waiting_for_human",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    queue = read_queue()
    queue.append(entry)
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(queue, indent=2) + "\n")
    return entry


def notify_team(priority: str, ticket_id: str = "") -> dict:
    """Stand-in for a real pager. In production this is PagerDuty / Slack."""
    channel = "pagerduty:support-oncall" if priority in ("urgent", "high") else "slack:#support-queue"
    print(f"[page] {channel} <- ticket {ticket_id or '?'} priority={priority}", file=sys.stderr)
    return {"channel": channel, "priority": priority, "delivered": True}
