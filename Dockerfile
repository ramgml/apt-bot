FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1


# RUN apt-get update && apt-get install -y \
#     gcc \
#     postgresql-client \
#     && rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

ENV UV_TOOL_BIN_DIR=/usr/local/bin

COPY pyproject.toml uv.lock /app/

RUN uv sync --locked --no-dev

COPY src/ /app/src/

ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONPATH="/app/src"
