"""Five tickets, five different paths through the graph."""

import json
from concurrent.futures import ThreadPoolExecutor

from rich.console import Console
from rich.panel import Panel

from graph import run_ticket
from tools.handoff import QUEUE_PATH
from trace import print_trace

console = Console(width=110)

TICKETS = [
    ("I was charged twice this month - two identical $490 charges on the same day. "
     "I want a refund for the duplicate.", "dana@northwind.io",
     "billing -> Account Agent finds the duplicate -> refund wording -> escalation"),

    ("How do I add a team member to my workspace?", "priya@lumen.dev",
     "account how-to -> Knowledge Agent only -> clean answer, high confidence"),

    ("Getting ERR_5012 every time I try to upload a video file.", "sam@arcadia.co",
     "technical -> Troubleshoot Agent chained into Knowledge Agent"),

    ("What is my current plan and how much usage have I got left this period?",
     "leo@bright.works",
     "account -> Account Agent tools: get_customer, usage_summary"),

    ("it's broken", "eli@quarrystone.net",
     "vague -> weak retrieval -> low confidence -> escalation with a handoff summary"),
]


def main() -> None:
    # start from an empty queue so GET /queue shows exactly this run
    QUEUE_PATH.write_text("[]\n")

    console.rule("[bold]Multi-agent support demo - 5 tickets[/bold]")
    console.print("[grey62]Running all five concurrently; trees print in order as they "
                  "finish.[/grey62]\n")

    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(run_ticket, text, email) for text, email, _ in TICKETS]
        results = []
        for (text, _, expected), future in zip(TICKETS, futures):
            result = future.result()
            results.append(result)
            console.print(f"[bold cyan]Expected path:[/bold cyan] [grey62]{expected}[/grey62]")
            print_trace(result)
            console.print(Panel(result["answer"], title="reply to customer",
                                border_style="grey42", width=110))
            console.print()

    console.rule("[bold]Summary[/bold]")
    for (text, _, _), result in zip(TICKETS, results):
        mark = "[red]ESCALATED[/red]" if result["escalated"] else "[green]ANSWERED [/green]"
        console.print(f'{mark}  #{result["ticket_id"]}  {result["category"]:<10} '
                      f'conf {result["confidence"]:.2f}  '
                      f'{len(result["tool_calls"])} tool calls  '
                      f'{result["latency_ms"]}ms  "{text[:40]}..."')

    queue = json.loads(QUEUE_PATH.read_text())
    waiting = ", ".join("#{} ({})".format(q["ticket_id"], q["priority"]) for q in queue)
    console.print(f"\n[bold]Human queue:[/bold] {len(queue)} ticket(s) waiting - "
                  f"{waiting or 'none'}")
    console.print("[grey62]Full traces written to traces/<ticket_id>.json[/grey62]")


if __name__ == "__main__":
    main()
