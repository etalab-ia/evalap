# Base stage: System dependencies that rarely change
FROM python:3.12-slim AS base

# Install system dependencies (supervisor, npm, nodejs) with BuildKit cache mount for faster builds
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    supervisor \
    npm \
    nodejs

# Install uv from official image (faster than pip install)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# UV configuration for optimal Docker builds
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_CACHE_DIR=/root/.cache/uv/python

# Dependencies stage: Python dependencies
FROM base AS dependencies

WORKDIR /app

# Copy only dependency files first for better caching
COPY ./pyproject.toml ./uv.lock /app/

# Install Python dependencies using uv sync with cache mount for faster rebuilds
# This layer is cached separately and only rebuilt when pyproject.toml or uv.lock changes
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Final stage: Application code
FROM dependencies AS final

# Copy application code
COPY ./docs /app/docs
COPY ./evalap /app/evalap
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /app
