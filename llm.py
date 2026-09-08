"""One shared LLM factory. Every agent goes through get_llm() / call_llm()."""

import json
import os
import re
import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "z-ai/glm-5.3-flash"


class LLMError(RuntimeError):
    pass


def get_llm(temperature: float = 0.0) -> ChatOpenAI:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise LLMError("OPENROUTER_API_KEY is not set. Put it in .env (see README).")
    return ChatOpenAI(
        model=os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL),
        api_key=key,
        base_url=BASE_URL,
        temperature=temperature,
        timeout=60,
        max_retries=1,
        # OpenRouter fans out across providers; pick the lowest-latency one
        extra_body={"provider": {"sort": "latency"}},
    )


def call_llm(system: str, user: str, temperature: float = 0.0) -> str:
    """Returns the model's text. Raises LLMError on any failure so callers can fall back."""
    try:
        reply = get_llm(temperature).invoke(
            [("system", system), ("human", user)]
        )
    except LLMError:
        raise
    except Exception as exc:
        raise LLMError(f"{type(exc).__name__}: {exc}") from exc
    text = reply.content if isinstance(reply.content, str) else str(reply.content)
    if not text.strip():
        raise LLMError("model returned an empty response")
    return text.strip()


def call_llm_json(system: str, user: str, temperature: float = 0.0) -> dict:
    raw = call_llm(system, user, temperature)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise LLMError(f"expected JSON, got: {raw[:120]}")
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise LLMError(f"bad JSON from model: {exc}") from exc


def warn_fallback(agent: str, exc: Exception) -> str:
    """Loud, visible degradation - never a silent swallow."""
    note = f"{agent}: LLM unavailable ({exc}) - using deterministic fallback"
    print(f"[warn] {note}", file=sys.stderr)
    return note
