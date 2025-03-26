FROM python:3.11-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . .

RUN uv sync --frozen --no-cache

CMD ["uv", "run", "python", "./main.py"]
