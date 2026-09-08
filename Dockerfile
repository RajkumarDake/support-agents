FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    langgraph langchain-openai langchain-core python-dotenv \
    rich rank-bm25 pydantic fastapi uvicorn httpx

COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
