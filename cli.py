"""CLI entry point: same graph, same trace, no HTTP."""

import argparse

from rich.console import Console
from rich.panel import Panel

from graph import run_ticket
from trace import TRACE_DIR, print_trace

console = Console(width=110)


def main() -> None:
    parser = argparse.ArgumentParser(prog="run.sh ask")
    parser.add_argument("text", help="the ticket text")
    parser.add_argument("--email", default="", help="customer email, if known")
    args = parser.parse_args()

    result = run_ticket(args.text, args.email)
    print_trace(result)
    console.print(Panel(result["answer"], title="reply to customer", border_style="grey42",
                        width=110))
    if result["escalated"]:
        console.print(Panel(result["handoff"]["summary"],
                            title=f'human handoff - priority {result["handoff"]["priority"]}',
                            border_style="red", width=110))
    console.print(f'[grey62]trace: {TRACE_DIR}/{result["ticket_id"]}.json[/grey62]')


if __name__ == "__main__":
    main()
