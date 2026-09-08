from typing import Any

DATA_DIR = "data"


def record(tool: str, args: dict[str, Any], result: str) -> dict[str, Any]:
    """Every tool call an agent makes is recorded in state['tool_calls'] with this shape."""
    return {"tool": tool, "args": args, "result": result}
