FROM python:3.12-slim

# UV installation and configuration
ENV UV_CACHE_DIR=/tmp/uv-cache \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
RUN pip install --no-cache-dir uv
# Setup files
WORKDIR /app
COPY ./pyproject.toml /app
COPY ./docs /app/docs
COPY ./evalap /app/evalap
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install dependency
# --
RUN uv pip install --no-cache --system .
# For the API and webapp
RUN apt-get update
RUN apt-get install -y supervisor
# For the doc
RUN apt-get install -y npm nodejs
RUN apt-get clean
