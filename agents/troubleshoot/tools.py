"""Troubleshoot Agent tools: the error-code book and the live incident board."""

import json
import pathlib
import re

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data"

_CODES: dict = {}
_INCIDENTS: list = []


def _load() -> None:
    global _CODES, _INCIDENTS
    if _CODES:
        return
    codes_path = DATA_DIR / "error_codes.json"
    incidents_path = DATA_DIR / "incidents.json"
    for path in (codes_path, incidents_path):
        if not path.exists():
            raise FileNotFoundError(f"missing data file: {path}")
    _CODES = json.loads(codes_path.read_text())
    _INCIDENTS = json.loads(incidents_path.read_text())


def extract_error_code(text: str) -> str | None:
    match = re.search(r"ERR[_-]?(\d{3,4})", text, re.IGNORECASE)
    return f"ERR_{match.group(1)}" if match else None


def lookup_error(code: str) -> dict | None:
    _load()
    return _CODES.get((code or "").upper().replace("-", "_"))


def known_issues(keyword: str = "", include_resolved: bool = False) -> list[dict]:
    """Open incidents, optionally filtered by a keyword or error code."""
    _load()
    key = (keyword or "").lower()
    out = []
    for inc in _INCIDENTS:
        if not include_resolved and inc["status"] == "resolved":
            continue
        haystack = " ".join([inc["title"], inc["summary"], " ".join(inc["affects"])]).lower()
        if key and key not in haystack:
            continue
        out.append({
            "id": inc["id"],
            "title": inc["title"],
            "status": inc["status"],
            "summary": inc["summary"],
            "workaround": inc["workaround"],
        })
    return out
