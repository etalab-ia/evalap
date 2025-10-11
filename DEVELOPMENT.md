# Development Setup with Hot Reloading

This guide explains how to run Evalap in development mode with full hot reloading for all services.

## Quick Start

### 1. Start the Development Environment

```bash
docker compose -f compose.dev.yml up --build
```

This will:
- Build the development Docker image (includes dev dependencies like `watchdog`)
- Start PostgreSQL database
- Run Alembic migrations
- Start all three services with hot reloading:
  - **Uvicorn API** on port 8000
  - **Runner** with file watching
  - **Streamlit UI** on port 8501

### 2. Access Your Services

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Streamlit UI**: http://localhost:8501
- **PostgreSQL**: localhost:5432 (credentials: postgres/changeme)

### 3. Start Coding!

Your code is live-mounted into the container. Any changes you make will automatically trigger reloads:

- **Edit API code** (e.g., `evalap/api/main.py`) → Uvicorn auto-reloads
- **Edit runner code** (e.g., `evalap/runners/tasks.py`) → Runner auto-restarts (you'll see `[Reloader]` messages)
- **Edit Streamlit code** (e.g., `evalap/ui/demo_streamlit/app.py`) → Streamlit prompts to rerun

## Hot Reloading Details

### Uvicorn (API)
- Uses the `--reload` flag
- Watches all Python files
- Reloads automatically on changes

### Streamlit (UI)
- Built-in file watching
- Prompts you to rerun when files change
- Can enable "Always rerun" in the UI

### Runner (Background Tasks)
- Uses custom hot-reload wrapper (`scripts/run_with_reload.py`)
- Watches all `.py` files in `evalap/` directory
- Implements 1-second debouncing to avoid rapid restarts
- Gracefully terminates and restarts the process
- Logs reload events with `[Reloader]` prefix

## Managing Services

### View Logs

```bash
# All services
docker compose -f compose.dev.yml logs -f

# Specific service
docker compose -f compose.dev.yml logs -f evalap_dev
```

### Control Processes Inside Container

```bash
# Enter the container
docker compose -f compose.dev.yml exec evalap_dev bash

# Check process status
supervisorctl status

# Restart a specific process
supervisorctl restart uvicorn
supervisorctl restart runner
supervisorctl restart streamlit

# View process logs
supervisorctl tail -f runner
supervisorctl tail -f uvicorn
supervisorctl tail -f streamlit
```

### Stop Services

```bash
docker compose -f compose.dev.yml down
```

### Rebuild After Dependency Changes

If you modify `pyproject.toml` or `uv.lock`:

```bash
docker compose -f compose.dev.yml up --build
```

## Differences from Production

The development setup differs from production in these ways:

| Feature | Development (`compose.dev.yml`) | Production (`Dockerfile`) |
|---------|--------------------------------|---------------------------|
| Dockerfile | `Dockerfile.dev` | `Dockerfile` |
| Supervisord Config | `supervisord.dev.conf` | `supervisord.conf` |
| Dependencies | Includes dev deps (watchdog, etc.) | Only production deps |
| Uvicorn | `--reload` (single worker) | `--workers 4` (multi-worker) |
| Runner | Hot-reload wrapper | Direct execution |
| Code Mounting | Live-mounted from host | Copied into image |

## Troubleshooting

### Hot Reload Not Working?

1. **Check volume mounting**: Ensure the volume is mounted correctly in `compose.dev.yml`
2. **Check logs**: Look for `[Reloader]` messages in runner logs
3. **Verify file changes**: Make sure you're editing files in the mounted directory

### Process Crashed?

```bash
# Check status
docker compose -f compose.dev.yml exec evalap_dev supervisorctl status

# View logs
docker compose -f compose.dev.yml logs evalap_dev

# Restart the service
docker compose -f compose.dev.yml restart evalap_dev
```

### Database Issues?

```bash
# Reset the database
docker compose -f compose.dev.yml down -v
docker compose -f compose.dev.yml up --build
```

## Environment Variables

Create a `.env` file in the project root to customize settings:

```bash
# Example .env
LOG_LEVEL=DEBUG
POSTGRES_URL=postgresql+psycopg2://postgres:changeme@postgres:5432/evalap_dev
```

The `.env` file is automatically loaded by Docker Compose.
