# PRD — Multi-Agent Customer Support Platform

Build this at `/home/ubuntu/projects/support-agents/`. It must RUN end to end tonight — it is being demoed in a live technical interview, screen-shared, and the author has to explain every file cold.

## 1. What it is

A customer support system built as a **LangGraph multi-agent state machine**. A support ticket comes in, a router agent classifies it, specialist agents handle it with their own tools, an evaluator gates the answer, and low-confidence or high-risk tickets escalate to a human queue.

**Story the author tells:** it started as a simple FAQ retrieval bot (one retriever, one answer step). Real tickets were not one shape — some need account data, some need troubleshooting steps, some need a human. A single chain could not branch or loop, so it was re-architected as a LangGraph graph with specialist agents and an escalation edge.

## 2. The six agents

Every one of these is an agent (a node in the graph with its own prompt, its own tools, its own failure mode). Do not collapse them into helper functions.

Every agent has tools. No agent is a bare LLM call.

1. **Router Agent** — reads the ticket, classifies it: `billing` | `technical` | `account` | `refund` | `unclear`. Outputs the category plus a short reason. Tools: `detect_sentiment(text)`, `check_priority_keywords(text)` (refund/legal/cancel/angry words bump priority). Falls back to a keyword heuristic if the LLM call fails.
2. **Knowledge Agent** — RAG over a help-doc corpus. Retrieves the top passages for the ticket with BM25 scoring over `corpus/` (ship 35-45 short markdown help docs across billing, technical, account, refunds, onboarding). Tools: `search_docs(query, k)`, `filter_by_category(cat)`.
3. **Account Agent** — looks up customer state from a shipped `data/customers.csv` and `data/invoices.csv`. Tools: `get_customer(email)`, `get_invoices(customer_id)`, `usage_summary(customer_id)`. Handles plan, subscription status, payment history, usage questions.
4. **Troubleshoot Agent** — technical issues. Tools: `lookup_error(code)` over a shipped `data/error_codes.json`, `known_issues()` over `data/incidents.json`, and it produces ordered fix steps.
5. **Response Agent** — writes the final customer-facing reply: correct tone, concrete, cites which doc or record it used. No invented facts — it only uses what earlier agents put in state. Tools: `get_template(category)`, `check_tone(draft)` (flags blame words, over-promising, missing greeting).
6. **Escalation Agent** — fires when the evaluator's confidence is low, or the ticket is a refund, or the sentiment is angry. Writes a handoff summary (what was tried, what is known, what the human needs to decide) and assigns a priority. Tools: `create_handoff(priority, summary)` (appends to `data/human_queue.json`), `notify_team(priority)` (logs the page-out).

Plus one control node:

- **Evaluator** — scores the drafted answer: are there sources, does it address the ticket, is confidence above threshold. This is the conditional edge that decides `respond` vs `escalate`.

## 3. Graph shape

```
ingest -> router -> (billing|account -> Account Agent)
                    (technical      -> Troubleshoot Agent)
                    (any            -> Knowledge Agent)
       -> Response Agent -> Evaluator --high--> respond
                                       --low---> Escalation Agent -> respond
```

- The state is a typed dict (`TypedDict` / pydantic) carrying: `ticket`, `customer_email`, `category`, `route_reason`, `docs[]`, `account_facts{}`, `tool_calls[]`, `draft`, `confidence`, `escalated`, `handoff`, `trace[]`.
- Knowledge Agent runs for most categories; Account and Troubleshoot are conditional. At least one path must chain two specialist agents so the demo shows multi-agent cooperation.
- The escalation edge must be a real conditional edge, not an if-statement inside one node.

## 4. LLM

Use **LangChain with OpenRouter**, model `z-ai/glm-5.3-flash`. The key is already in `/home/ubuntu/projects/support-agents/.env` as `OPENROUTER_API_KEY` — load it with python-dotenv, never hardcode it, and make sure `.env` is in `.gitignore`.

Use `ChatOpenAI` from `langchain-openai` pointed at `https://openrouter.ai/api/v1`. One shared factory function `get_llm()` — every agent uses it, no per-agent duplication. Temperature 0 for router/evaluator, 0.3 for response.

If the API call fails, each agent degrades to a deterministic fallback (keyword routing, template response) so a demo never dies on a network blip.

## 5. Observability

Every agent appends a span to `state["trace"]`: `{agent, latency_ms, input_summary, output_summary}`. After the run, print a tree to the terminal with the `rich` library:

```
Ticket #4821  "I was charged twice this month"
├─ Router Agent          412ms   category=billing
├─ Account Agent         180ms   tools: get_customer, get_invoices
├─ Knowledge Agent       220ms   3 docs matched
├─ Response Agent        890ms   draft 412 chars
├─ Evaluator              15ms   confidence 0.38 LOW
└─ Escalation Agent      340ms   priority=high -> human queue
                                 total 2057ms
```

Also write the full trace JSON to `traces/<ticket_id>.json`.

## 6. How tickets get in

Two entry points, same graph behind both.

**A) HTTP API (`api.py`, FastAPI on port 8000)** — this is what gets screen-shared.

- `POST /ticket` body `{"text": "...", "email": "a@b.com"}` -> returns `{ticket_id, category, answer, confidence, escalated, agents_used[], trace[], latency_ms}`
- `GET /ticket/{id}` -> stored result and full trace
- `GET /queue` -> the human escalation queue
- `GET /health`
- Serve a tiny single-page HTML at `/` — one textarea, one email field, a submit button, and the agent trace rendered as a list with timings. Plain HTML/CSS/JS in one file, no build step, no framework. It must look clean, not like a debug dump.

**B) CLI** — `./run.sh ask "ticket text" --email a@b.com` runs the same graph in-process and prints the trace tree.

In the README, note how this would be fed in production: a Zendesk/Freshdesk webhook posting to `/ticket`, or an IMAP poller on the support inbox turning new mail into ticket payloads. Do NOT build the mail poller — just state it as the integration point, and keep `POST /ticket` as the seam that makes it trivial.

## 7. Demo

`demo.py` runs five tickets, each exercising a different path:
1. Double charge (billing) -> Account Agent -> refund keyword -> escalation
2. "How do I add a team member?" (account/how-to) -> Knowledge Agent -> clean answer, high confidence
3. "Getting ERR_5012 on upload" (technical) -> Troubleshoot Agent + Knowledge Agent chained
4. "What is my current plan and usage?" (account) -> Account Agent tools
5. A vague one-liner ("it's broken") -> low confidence -> escalation with a handoff summary

`run.sh`:
- `./run.sh demo` — all five tickets with trace trees
- `./run.sh serve` — start the FastAPI app on port 8000 (uvicorn)
- `./run.sh ask "ticket text" [--email a@b.com]` — one ticket interactively
- `./run.sh setup` — create the venv and install deps

Venv at `venv/` (python3.11): langgraph, langchain-openai, langchain-core, python-dotenv, rich, rank-bm25, pydantic, fastapi, uvicorn, httpx.

## 7. Code style — IMPORTANT

- **Simple, short code.** No metaprogramming, no clever abstractions, no deep class hierarchies. A reader should follow any file top to bottom in one pass.
- **Comments: add them, but sparingly.** One line above a non-obvious block. No comment walls, no docstring essays, no explaining what the next line literally does.
- Clear module split: `agents/router.py`, `agents/knowledge.py`, `agents/account.py`, `agents/troubleshoot.py`, `agents/response.py`, `agents/escalation.py`, `graph.py`, `state.py`, `llm.py`, `tools/`, `api.py`, `demo.py`.
- Fail loudly with clear messages; do not silently swallow errors.

## 8. Git

`git init`, commit as you go. **Commit messages: short, lowercase, one line, no body.** Examples: `add router agent`, `wire escalation edge`, `bm25 retrieval`, `trace tree output`.

**Do NOT add "Co-Authored-By", "Generated with Claude Code", or any attribution trailer to any commit.** Set `user.name="Rajkumar Dake"` and `user.email=rajkumardakey831@gmail.com`.

Create a private GitHub repo `support-agents` with `gh repo create support-agents --private --source=. --push` (gh is already authenticated as RajkumarDake) and push at the end.

## 9. Docs to produce

- `README.md` — what it is, the ASCII graph diagram, how to run, and a short design-decisions section: why a graph instead of a chain, why separate agents instead of one prompt, how escalation works, what the traces give you.
- `INTERVIEW_NOTES.md` — one page: a 60-second spoken explanation of the system, and the 6 questions an interviewer will ask with tight answers (why six agents and not one LLM call, how the router decides, why LangGraph over a chain, what happens when an agent fails, how you would scale this to separate services, how you would measure it in production). Also list the exact commands to run during a screen share.

## 10. Definition of done

Run `./run.sh demo` yourself and confirm all five tickets complete, the routing differs per ticket, tools actually fire, at least one ticket escalates, and the trace trees print.

Then start the API (`./run.sh serve`), and verify with curl: `POST /ticket` returns a real answer with a trace, `GET /queue` shows the escalated ticket, `GET /` serves the UI page. Confirm the UI renders (fetch it and check the HTML, or screenshot it).

Report what runs, the exact demo commands, and anything the author should be careful claiming.
