FROM python:3.12-slim

# Setup files
WORKDIR /app
COPY ./pyproject.toml /app
COPY ./docs /app/docs
COPY ./evalap /app/evalap
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install dependency
RUN pip install --no-cache-dir .
RUN apt-get update
# For the API and webapp 
RUN apt-get install -y supervisor
# For the doc
RUN apt-get install -y npm nodejs
RUN apt-get clean
