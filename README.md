# Multi-Agent Customer Support

A support system built as a LangGraph state machine. A mail comes in, the router agent splits it
into separate problems and sends a sub-query to the agent that can solve each one. Every agent
works its own piece with its own tools and reports its findings back. The response agent collects
all of them and writes one reply.

![the UI after one ticket](docs/screenshot.png)

## The graph

```mermaid
flowchart TD
    A[Router Agent] -->|sub-query 1| B[Knowledge Agent]
    A -->|sub-query 2| C[Account Agent]
    A -->|sub-query 3| D[Troubleshoot Agent]
    A -->|risk| E[Escalation Agent]

    B -->|findings| F[Response Agent]
    C -->|findings| F
    D -->|findings| F
    E -->|handoff| F

    F --> G[one reply to the customer]

    style A fill:#1f2937,stroke:#60a5fa,color:#fff
    style E fill:#1f2937,stroke:#f87171,color:#fff
    style F fill:#1f2937,stroke:#fbbf24,color:#fff
    style G fill:#1f2937,stroke:#34d399,color:#fff
```

The router does not pick one path, it fans out. A mail saying *"I was charged twice and my
uploads fail with ERR_5012"* is two problems, so it produces two sub-queries:

```python
[{"agent": "account",      "query": "check for duplicate charges", "details": {"email": "..."}},
 {"agent": "troubleshoot", "query": "upload fails with ERR_5012",  "details": {"error_code": "ERR_5012"}}]
```

The account agent never sees the upload problem, the troubleshoot agent never sees the billing
one. Each gets only its own question and the details it needs.

Both run in the same LangGraph superstep and append their findings to `state["results"]`, an
append-only channel, so parallel writes merge instead of clobbering each other. Agents that were
not dispatched never run.

The response agent then reads every result in state and writes a single reply that answers every
problem, citing the record ids and doc ids the agents actually found.

## The agents

| Agent | Job | Tools |
|---|---|---|
| **Router** | split the mail, dispatch sub-queries, classify the ticket | `detect_sentiment`, `check_priority_keywords` |
| **Knowledge** | BM25 retrieval over 55 help docs | `search_docs`, `filter_by_category` |
| **Account** | plan, invoices, usage; flags duplicate charges | `get_customer`, `get_invoices`, `usage_summary` |
| **Troubleshoot** | match error codes and open incidents, order fix steps | `lookup_error`, `known_issues` |
| **Response** | merge results into one cited reply | `get_template`, `check_tone` |
| **Escalation** | write the human handoff, set priority, queue it | `create_handoff`, `notify_team` |

Every agent has a deterministic fallback. With the API key removed the whole graph still
completes in under half a second with a grounded, cited answer.

## When a human takes over

Escalation is not a separate stage after the answer - it is one of the agents the router can
dispatch. Refunds, angry customers and high-priority wording get an escalation dispatch
alongside the specialists, so the facts still get gathered while the handoff is written.

The Escalation Agent writes the note a human reads first (what the customer wants, why it needs
a human, what to decide), queues it with a priority and an SLA, and pages the on-call channel.
Its result goes into `state["results"]` like any other agent, so the Response Agent folds it into
the same reply: the customer gets the facts *and* is told a specialist is picking it up.

So a ticket can produce a complete, cited answer and still be handed to a human. The
double-charge mail does exactly that, because refunds are a money decision.

## Run it

```bash
python3.11 -m venv venv
venv/bin/pip install langgraph langchain-openai langchain-core python-dotenv rich \
  rank-bm25 pydantic fastapi uvicorn httpx

echo "OPENROUTER_API_KEY=sk-or-..." > .env
venv/bin/python server.py          # http://localhost:8000
```

```bash
curl -s localhost:8000/health

curl -s -X POST localhost:8000/ticket -H "Content-Type: application/json" \
  -d '{"text":"I was charged twice this month and my uploads keep failing with ERR_5012","email":"dana@northwind.io"}'

curl -s localhost:8000/queue
```

The server logs the full agent trace for every ticket:

```
Ticket #6102  "I was charged twice this month and my uploads keep failing..."
├── Router Agent          4701ms  dispatched: account, troubleshoot | category=refund
├── Account Agent          822ms  tools: get_customer, get_invoices | duplicate INV-8804/INV-8805
├── Troubleshoot Agent    4595ms  tools: lookup_error, known_issues | ERR_5012 + INC-2291
├── Response Agent        6465ms  merged 2 agent results, draft 1189 chars
└── Escalation Agent      7939ms  priority=high -> human queue (sla 4h)
   ESCALATED  total 25904ms
```

Each trace is also written to `traces/<ticket_id>.json`.

## API

| Endpoint | Purpose |
|---|---|
| `GET /` | single-page UI |
| `GET /health` | liveness |
| `POST /ticket` | `{text, email}` -> answer, category, dispatches, agents used, trace |
| `GET /ticket/{id}` | stored result and trace |
| `GET /queue` | human escalation queue |

In production a Zendesk/Freshdesk webhook or an IMAP poller on the support inbox posts to
`POST /ticket`. That endpoint is the only integration seam.

## Design decisions

**Graph, not a chain.** A chain cannot branch to a variable set of agents and cannot route to a
different terminal based on a later node's output. The router's fan-out and the escalation
edge both need a graph.

**Separate agents, not one prompt.** Each agent has its own tools, its own prompt and its own
failure mode. When something is wrong the trace says which agent, not "the LLM was wrong".

**Tools next to their agent.** `agents/<name>/agent.py` is the node, `agents/<name>/tools.py`
is what it can do. Adding an agent is a new folder plus one dispatch entry.

**Traces first.** Every agent records a span. Without it, debugging a multi-agent run is
guesswork across scattered logs.

## Layout

```
server.py           entry point
api.py              FastAPI routes
graph.py            LangGraph wiring, fan-out, conditional edge
state.py            typed state
llm.py              OpenRouter client (glm-5.3-flash) + fallback
trace.py            spans, trace tree, JSON output
agents/<name>/      agent.py + tools.py
corpus/             55 help docs
data/               customers, invoices, error codes, incidents, human queue
static/index.html   UI
```
