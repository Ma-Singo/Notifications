# ==================
# Builder stage
# ==================
# ARG TARGETPLATFORM
# FROM --targetplatform=$TARGETPLATFORM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_VENV_IN_PROJECT=1

COPY pyproject.toml uv.lock ./

RUN uv sync \
    --frozen \
     --no-dev \
     --no-install-project


# ==================
# Runtime stage
# ==================

FROM python:3.12-slim
# FROM --targetplatform=$TARGETPLATFORM python:3.12-slim

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:${PATH}"

COPY . .

EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
