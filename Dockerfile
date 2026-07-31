FROM python:3.11-slim AS builder
ENV POETRY_VERSION=2.4.1
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true && poetry install --no-root --only main

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY agdbot-anonymous-telegram-board/ ./agdbot-anonymous-telegram-board/
CMD ["/app/.venv/bin/python", "agdbot-anonymous-telegram-board/main.py"]
