# Base stage: Start with Node.js (already includes npm and nodejs)
FROM node:20-slim AS base

# No additional system dependencies needed!
# node:20-slim already includes Node.js, npm, and SSL/TLS support for uv

# Install uv from official image
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# UV configuration for optimal Docker builds
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_CACHE_DIR=/root/.cache/uv/python

# Install Python 3.12 using uv (fast!)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv python install 3.12

# Dependencies stage: Python dependencies
FROM base AS dependencies

WORKDIR /app

# Copy only dependency files first for better caching
COPY ./pyproject.toml ./uv.lock /app/

# Install Python dependencies using uv sync with cache mount for faster rebuilds
# This layer is cached separately and only rebuilt when pyproject.toml or uv.lock changes
# uv sync creates a virtual environment by default at .venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Add the virtual environment to PATH so Python and packages are accessible
ENV PATH="/app/.venv/bin:$PATH"

# Final stage: Application code
FROM dependencies AS final

# Copy application code
COPY ./docs /app/docs
COPY ./evalap /app/evalap
COPY supervisord.conf /app/supervisord.conf

WORKDIR /app
