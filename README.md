# Multi-Agent Customer Support

A support system built as a LangGraph state machine. A ticket comes in, a router agent splits
it into problems and dispatches a sub-query to every agent needed, each agent solves its piece
with its own tools, and risky tickets go to a human instead of being auto-answered.

![the UI after one ticket](docs/screenshot.png)

## The graph

```mermaid
flowchart TD
    A[Router Agent] -->|sub-query| B[Knowledge Agent]
    A -->|sub-query| C[Account Agent]
    A -->|sub-query| D[Troubleshoot Agent]

    B --> E[Response Agent]
    C --> E
    D --> E

    E -->|refund / angry / high priority| F[Escalation Agent]
    E -->|everything else| G[respond]
    F --> G

    style A fill:#1f2937,stroke:#60a5fa,color:#fff
    style E fill:#1f2937,stroke:#fbbf24,color:#fff
    style F fill:#1f2937,stroke:#f87171,color:#fff
    style G fill:#1f2937,stroke:#34d399,color:#fff
```

The router fans out, it does not pick one path. A mail saying *"I was charged twice and my
uploads fail with ERR_5012"* dispatches two sub-queries:

```python
[{"agent": "account",      "query": "check for duplicate charges", "details": {"email": "..."}},
 {"agent": "troubleshoot", "query": "upload fails with ERR_5012",  "details": {"error_code": "ERR_5012"}}]
```

Both agents run in the same LangGraph superstep and append to `state["results"]`, an append-only
channel, so parallel writes merge instead of clobbering. Agents that were not dispatched never
run. The Response Agent merges every result into one reply that answers every problem.

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

Not every ticket should be answered automatically. After the Response Agent merges the results,
one check decides the terminal: refunds, angry customers and high-priority keywords go to the
Escalation Agent, everything else goes straight out.

The Escalation Agent does not just set a flag. It writes the handoff note a human reads first -
what the customer wants, what the agents already found with record ids, and the judgement call
the automation cannot make - then queues it with a priority and an SLA.

So a reply can be well written and still escalate. The double-charge ticket produces a complete,
cited answer and *still* goes to a human, because refunds are a money decision.

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
