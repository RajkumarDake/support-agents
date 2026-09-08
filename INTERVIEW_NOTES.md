# Interview notes

## The 60-second version

"This is a customer support system built as a LangGraph state machine. It started as an FAQ
retrieval bot - one retriever, one answer step - and that broke as soon as real tickets arrived,
because tickets are not one shape. A billing question needs the customer's invoices, a technical
one needs an error-code lookup, and a refund needs a human. A chain can't branch or loop, so I
rebuilt it as a graph.

A ticket hits the router agent, which classifies it and decides whether we need this customer's
records. Technical tickets go to a troubleshoot agent that matches the error code and any open
incident. Billing and account tickets go to an account agent that reads real invoice and usage
rows. Both chain into a knowledge agent doing BM25 retrieval over the help corpus, so the writer
always has citations. A response agent drafts the reply using only what's in state - it can't
invent an invoice ID because it never sees anything but the retrieved facts.

Then an evaluator scores the draft, and that score drives a conditional edge: high confidence
goes out to the customer, low confidence or a refund or an angry customer goes to an escalation
agent that writes a handoff note and puts it on a human queue with a priority and an SLA.

Every agent writes a span into the trace, so I get a tree showing which path the ticket took,
what each step cost, and what it cited. And every agent has a deterministic fallback - pull the
API key and the whole graph still runs, in about 300 milliseconds, with a template answer."

## Six questions and the answers

**1. Why six agents and not one LLM call with all the tools attached?**
Because I want to know *which* part failed. One prompt with six tools gives you one output and no
way to tell misrouting from bad retrieval from bad writing. Six nodes give me a trace with a span
per step, an independent failure mode per step, and independent testability - the account agent
can lose the LLM entirely and still return real invoice rows from CSV. It also means I can tune
one prompt without regression-testing the other five. The cost is latency: six sequential calls
instead of one. That is the trade I made, and the trace is what buys it back.

**2. How does the router actually decide?**
Two deterministic tools run first: `detect_sentiment` and `check_priority_keywords`. Their output
goes into the prompt, so the LLM classifies with the risk signals already in front of it. It
returns a category, a one-line reason, and a `needs_account_data` boolean - "does answering this
require looking up *this* customer's records?" That boolean is what separates "how do I add a
team member" (a doc question, knowledge only) from "what's my plan and usage" (a records
question, account agent first). If the LLM call fails or returns a category outside the enum, a
keyword table routes it instead. And there's one hard override: if the ticket contains refund
wording, it is a refund ticket regardless of what the model said.

**3. Why LangGraph rather than a chain, or plain Python?**
Two things a chain can't express: conditional branching and a second terminal path. Plain Python
could do both, obviously - but then routing lives inside functions as scattered `if` statements.
LangGraph makes the edges declarative, so the whole control flow is readable in twenty lines of
`build_graph()`. I get typed shared state with reducers (the trace and tool-call lists are
append-only channels, so nodes return only their own entries), and the escalation policy is one
named function on an edge that a support lead could review. It also gives me somewhere obvious to
add checkpointing and human-in-the-loop resume later, which is the actual next step.

**4. What happens when an agent fails?**
Every agent catches `LLMError` only - not bare `except` - prints a `[warn]` line to stderr naming
the agent and the exception, and drops to a deterministic fallback: keyword routing, verbatim
error-code steps, a template reply, deterministic-only confidence. Failures are visible in the
trace, never silent. I tested this by running the graph with a bad API key: all five demo paths
still complete, with grounded answers, in a few hundred milliseconds. What is *not* handled is a
partial failure inside a tool - if `customers.csv` is missing, that raises and the request fails,
deliberately, because a support answer built on missing account data is worse than an error.

**5. How would you scale this to separate services?**
The state is already a serialisable typed dict and the agents already only touch state, so each
node becomes an HTTP handler or a queue consumer with almost no change. The realistic split is by
resource, not by agent: the retrieval agent becomes a search service, the account agent becomes a
thin client over the real billing API with its own auth and rate limits, and the LLM-heavy nodes
scale independently because they're the slow ones. LangGraph gets a checkpointer (Postgres or
Redis) so a run can suspend on escalation and resume when the human answers, instead of finishing
in one process. The escalation queue becomes a real queue and `notify_team` becomes PagerDuty.
The one thing I would not split is router and evaluator - they're cheap and they're the control
plane.

**6. How would you measure this in production?**
Three layers. Offline: a labelled set of tickets with expected categories, so routing accuracy is
a number and prompt changes are regression-tested. Online proxies: escalation rate, evaluator
confidence distribution, retrieval hit rate, and per-agent p50/p95 latency - all of which come
straight out of the trace JSON that's already being written. Ground truth: reply-again rate (did
the customer come back within 24 hours, the real signal that the answer was wrong), human
override rate on escalated tickets, and CSAT. The metric I would watch hardest is the gap between
evaluator confidence and human override - if we're confidently wrong, the threshold is miscalibrated,
and that is the one failure mode that actually costs you customers.

## Screen-share script

```bash
cd support-agents

# 1. the five paths, ~90 seconds, tickets run concurrently
./run.sh demo

# 2. one ticket interactively - point at the trace tree and the handoff panel
./run.sh ask "I was charged twice this month, I want a refund" --email dana@northwind.io

# 3. the API + UI
venv/bin/python server.py
#    open http://localhost:8000, click the "double charge" chip, Run agents

# 4. in another terminal, the same graph over HTTP
curl -s -X POST localhost:8000/ticket -H 'Content-Type: application/json' \
  -d '{"text":"Getting ERR_5012 on upload","email":"sam@arcadia.co"}' | python3 -m json.tool
curl -s localhost:8000/queue | python3 -m json.tool
curl -s localhost:8000/health

# 5. the money shot - kill the LLM and show it still works
OPENROUTER_API_KEY=broken ./run.sh ask "Getting ERR_5012 on upload" --email sam@arcadia.co
```

Files to have open: `graph.py` (the edges), `agents/evaluator.py` (the escalation edge),
`agents/router.py` (tools before the LLM call, fallback after).

## Things to be careful claiming

- The corpus, customer records and incidents are **fixture data written for this demo**, not a
  real help centre.
- `notify_team` prints a line. It does not page anyone.
- Confidence is a **heuristic blend**, not a calibrated probability. It has not been validated
  against human judgements - there is no labelled set here.
- There are no automated tests in this repo. The verification is the demo run and the fallback
  run.
- A live ticket takes 25-90 seconds, and the spread is wide. It is six sequential calls to a
  reasoning model that cannot be told to skip its reasoning; latency is provider-dependent.
