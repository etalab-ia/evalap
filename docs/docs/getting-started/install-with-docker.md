---
sidebar_position: 1
---

# Install with Docker

This guide will walk you through the process of installing and running Evalap using Docker.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker version 18.0.6 or above.

## Run with compose

Create a `compose.yml` file with the following content:

```yaml
services:
  postgres:
    image: postgres:16.5
    restart: always
    user: postgres
    environment:
      - TZ=Europe/Paris
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres_password
      - POSTGRES_DB=evalap
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready", "-U", "postgres"]
      interval: 4s
      timeout: 10s
      retries: 5
      start_period: 60s

  evalap:
    image: ghcr.io/etalab-ia/evalap/evalap:main-latest
    restart: always
    environment:
      - TZ=Europe/Paris
      - ENV=prod
      - DB_NAME=${DB_NAME:-evalap}
      - POSTGRES_URL=${POSTGRES_URL:-postgresql://postgres:postgres_password@postgres:5432/evalap}
      - ADMIN_TOKEN=${ADMIN_TOKEN}
      - MFS_API_KEY_V2=${MFS_API_KEY_V2}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
      - ALBERT_API_KEY=${ALBERT_API_KEY}
    ports:
      - "8000:8000"
      - "8501:8501"
      - "3000:3000"
    volumes:
      - evalap_data:/data
    command: ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
    depends_on:
      postgres:
        condition: service_started

volumes:
  postgres_data:
  evalap_data:
```

Then run the application with:

```bash
docker compose up -d
```

This will start both the application and the database services in detached mode.

You should then be able to connect to the following services:
- the API at http://localhost:8000/docs
- the webapp at http://localhost:8501


## Next Steps

Now that you have Evalap installed with Docker, you can:

- [Add your dataset](../user-guides/add-your-dataset.md) to start evaluating models
- [Create a simple experiment](../user-guides/create-a-simple-experiment.md) to test the platform
- Explore the Jupyter notebook examples in the `notebooks/` directory
