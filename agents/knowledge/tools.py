"""Knowledge Agent tools: BM25 retrieval over the markdown help corpus in corpus/."""

import pathlib
import re

from rank_bm25 import BM25Okapi

CORPUS_DIR = pathlib.Path(__file__).resolve().parents[2] / "corpus"

_DOCS: list[dict] = []
_BM25: BM25Okapi | None = None

STOPWORDS = {"the", "a", "an", "is", "are", "was", "were", "to", "of", "and", "or", "in",
             "on", "for", "it", "my", "i", "we", "you", "this", "that", "with", "at",
             "be", "have", "has", "do", "does", "did", "can", "how", "what", "why", "me"}


def _stem(word: str) -> str:
    """Crude suffix stripping so 'charged'/'charges' match 'charge'."""
    for suffix in ("ing", "ed", "es", "s"):
        if len(word) > 4 and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9_]+", text.lower())
    return [_stem(w) for w in words if w not in STOPWORDS]


def _load() -> None:
    """Read every corpus/*.md once and build the BM25 index."""
    global _BM25
    if _DOCS:
        return
    files = sorted(CORPUS_DIR.glob("*.md"))
    if not files:
        raise FileNotFoundError(f"no help docs found in {CORPUS_DIR}")
    for path in files:
        raw = path.read_text()
        title = re.search(r"^title:\s*(.+)$", raw, re.MULTILINE)
        category = re.search(r"^category:\s*(.+)$", raw, re.MULTILINE)
        body = raw.split("---", 2)[-1].strip()
        _DOCS.append({
            "id": path.stem,
            "title": title.group(1).strip() if title else path.stem,
            "category": category.group(1).strip() if category else "general",
            "body": body,
        })
    _BM25 = BM25Okapi([_tokenize(d["title"] + " " + d["body"]) for d in _DOCS])


def search_docs(query: str, k: int = 3, category: str | None = None) -> list[dict]:
    """Top-k passages by BM25. An optional category restricts the candidate pool."""
    _load()
    scores = _BM25.get_scores(_tokenize(query))
    pool = range(len(_DOCS))
    if category:
        narrowed = [i for i in pool if _DOCS[i]["category"] == category]
        # only narrow if the category actually has documents
        pool = narrowed or pool
    ranked = sorted(pool, key=lambda i: scores[i], reverse=True)[:k]
    return [{
        "id": _DOCS[i]["id"],
        "title": _DOCS[i]["title"],
        "category": _DOCS[i]["category"],
        "score": round(float(scores[i]), 2),
        "excerpt": _excerpt(_DOCS[i]["body"]),
    } for i in ranked if scores[i] > 0]


def filter_by_category(cat: str) -> list[dict]:
    _load()
    return [{"id": d["id"], "title": d["title"]} for d in _DOCS if d["category"] == cat]


def _excerpt(body: str, limit: int = 420) -> str:
    text = re.sub(r"^#.*$", "", body, flags=re.MULTILINE).strip()
    text = re.sub(r"\s+", " ", text)
    return text[:limit] + ("..." if len(text) > limit else "")


def corpus_size() -> int:
    _load()
    return len(_DOCS)
