FROM python:3.12-slim

# UV installation and configuration
ENV UV_CACHE_DIR=/tmp/uv-cache \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
RUN pip install --no-cache-dir uv
# Setup files
WORKDIR /app
COPY ./pyproject.toml /app
COPY ./evalap /app/evalap
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install dependency
RUN uv pip install --no-cache --system .
RUN apt-get update && apt-get install -y supervisor && apt-get clean
