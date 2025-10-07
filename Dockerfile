# Base stage: System dependencies that rarely change
FROM python:3.12-slim AS base

# Install system dependencies (supervisor, npm, nodejs)
# These are cached separately and only rebuilt when this layer changes
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    supervisor \
    npm \
    nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# UV installation and configuration
ENV UV_CACHE_DIR=/tmp/uv-cache \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
RUN pip install --no-cache-dir uv

# Dependencies stage: Python dependencies
FROM base AS dependencies

WORKDIR /app

# Copy only dependency files first for better caching
COPY ./pyproject.toml ./uv.lock /app/

# Install Python dependencies using uv sync
# This layer is cached separately and only rebuilt when pyproject.toml or uv.lock changes
RUN uv sync --locked --no-dev

# Final stage: Application code
FROM dependencies AS final

# Copy application code
COPY ./docs /app/docs
COPY ./evalap /app/evalap
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /app
