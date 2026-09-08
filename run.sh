#!/usr/bin/env bash
# Entry point for everything: setup, demo, serve, ask.
set -euo pipefail

cd "$(dirname "$0")"
PY=venv/bin/python

need_venv() {
  if [ ! -x "$PY" ]; then
    echo "venv missing - run ./run.sh setup first" >&2
    exit 1
  fi
}

case "${1:-}" in
  setup)
    python3.11 -m venv venv
    venv/bin/pip install --upgrade pip
    venv/bin/pip install langgraph langchain-openai langchain-core python-dotenv rich \
      rank-bm25 pydantic fastapi uvicorn httpx
    echo "setup done. put OPENROUTER_API_KEY in .env, then: ./run.sh demo"
    ;;

  demo)
    need_venv
    exec "$PY" demo.py
    ;;

  serve)
    need_venv
    exec venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000
    ;;

  ask)
    need_venv
    shift
    exec "$PY" cli.py "$@"
    ;;

  *)
    cat <<'USAGE'
usage:
  ./run.sh setup                          create venv and install deps
  ./run.sh demo                           run the five demo tickets with trace trees
  ./run.sh serve                          start the API + UI on http://localhost:8000
  ./run.sh ask "ticket text" [--email a@b.com]
USAGE
    exit 1
    ;;
esac
