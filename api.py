"""FastAPI front door. POST /ticket is the seam a helpdesk webhook would post to."""

import json
import logging
import pathlib

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from agents.escalation.tools import read_queue
from graph import run_ticket
from trace import TRACE_DIR, print_trace

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("support")

HERE = pathlib.Path(__file__).resolve().parent
app = FastAPI(title="Support Agents", version="1.0")

# in-process cache; the trace files on disk are the durable copy
RESULTS: dict[str, dict] = {}


class TicketIn(BaseModel):
    text: str = Field(min_length=1)
    email: str = ""


@app.get("/")
def index() -> FileResponse:
    return FileResponse(HERE / "static" / "index.html")


@app.get("/health")
def health() -> dict:
    log.info("GET /health")
    return {"status": "ok"}


@app.post("/ticket")
def create_ticket(payload: TicketIn) -> dict:
    log.info("POST /ticket email=%s text=%r", payload.email or "-", payload.text[:80])
    result = run_ticket(payload.text, payload.email)
    RESULTS[result["ticket_id"]] = result
    print_trace(result)
    log.info(
        "ticket %s category=%s agents=%s escalated=%s %dms",
        result["ticket_id"], result["category"], ",".join(result["agents_used"]),
        result["escalated"], result["latency_ms"],
    )
    return {
        "ticket_id": result["ticket_id"],
        "category": result["category"],
        "route_reason": result["route_reason"],
        "dispatches": result["dispatches"],
        "answer": result["answer"],
        "escalated": result["escalated"],
        "agents_used": result["agents_used"],
        "tool_calls": result["tool_calls"],
        "trace": result["trace"],
        "latency_ms": result["latency_ms"],
    }


@app.get("/ticket/{ticket_id}")
def get_ticket(ticket_id: str) -> dict:
    if ticket_id in RESULTS:
        return RESULTS[ticket_id]
    path = TRACE_DIR / f"{ticket_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"no ticket {ticket_id}")
    return json.loads(path.read_text())


@app.get("/queue")
def queue() -> dict:
    entries = read_queue()
    return {"depth": len(entries), "queue": entries}
