"""Account Agent tools: read-only lookups over the shipped customer records."""

import csv
import pathlib
from collections import Counter

DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"

_CUSTOMERS: list[dict] = []
_INVOICES: list[dict] = []


def _load() -> None:
    if _CUSTOMERS:
        return
    for path, target in ((DATA_DIR / "customers.csv", _CUSTOMERS),
                         (DATA_DIR / "invoices.csv", _INVOICES)):
        if not path.exists():
            raise FileNotFoundError(f"missing data file: {path}")
        with path.open() as fh:
            target.extend(csv.DictReader(fh))


def get_customer(email: str) -> dict | None:
    _load()
    email = (email or "").strip().lower()
    for row in _CUSTOMERS:
        if row["email"].lower() == email:
            return {
                "customer_id": row["customer_id"],
                "name": row["name"],
                "email": row["email"],
                "company": row["company"],
                "plan": row["plan"],
                "status": row["status"],
                "renewal_date": row["renewal_date"],
                "payment_method": row["payment_method"],
            }
    return None


def get_invoices(customer_id: str, limit: int = 6) -> list[dict]:
    _load()
    rows = [r for r in _INVOICES if r["customer_id"] == customer_id]
    rows.sort(key=lambda r: r["date"], reverse=True)
    return [{
        "invoice_id": r["invoice_id"],
        "date": r["date"],
        "amount_usd": float(r["amount_usd"]),
        "status": r["status"],
        "description": r["description"],
    } for r in rows[:limit]]


def usage_summary(customer_id: str) -> dict | None:
    _load()
    row = next((r for r in _CUSTOMERS if r["customer_id"] == customer_id), None)
    if not row:
        return None
    api_pct = round(100 * int(row["api_calls_used"]) / max(int(row["api_calls_limit"]), 1))
    storage_pct = round(100 * float(row["storage_gb_used"]) / max(float(row["storage_gb_limit"]), 1))
    return {
        "plan": row["plan"],
        "seats": f'{row["seats_used"]} of {row["seats_included"]}',
        "api_calls": f'{int(row["api_calls_used"]):,} of {int(row["api_calls_limit"]):,} ({api_pct}%)',
        "storage": f'{row["storage_gb_used"]} GB of {row["storage_gb_limit"]} GB ({storage_pct}%)',
        "near_limit": [name for name, pct in (("api_calls", api_pct), ("storage", storage_pct))
                       if pct >= 80],
    }


def find_duplicate_charges(invoices: list[dict]) -> list[dict]:
    """Two settled invoices with the same date and amount are a duplicate charge."""
    seen = Counter((i["date"], i["amount_usd"]) for i in invoices if i["status"] == "paid")
    dupes = {key for key, count in seen.items() if count > 1}
    return [i for i in invoices if (i["date"], i["amount_usd"]) in dupes]
