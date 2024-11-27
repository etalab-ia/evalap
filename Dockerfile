FROM python:3.12-slim

# Setup files
WORKDIR /app
COPY ./pyproject.toml /app
COPY ./api /app/api
COPY ./ui /app/ui
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install dependency
RUN pip install --no-cache-dir .
RUN apt-get update && apt-get install -y supervisor && apt-get clean
