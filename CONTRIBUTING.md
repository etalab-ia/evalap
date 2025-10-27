# Contributing to EvalAP

## Project Architecture

The stack is based on Fastapi+pydantic+sqlachemy for the API in conjonction with ZeroMQ for the Runner.
The project includes an UI/UX based on Streamlit [WIP].

```
evalap/
├── justfile    --> just is a handy way to save and run project-specific commands. See https://just.systems
├── evalap/        --> The evalap code source
│   ├── api/        --> The evaluation API source code
│   ├── runner/     --> The runner (message passing) source code
│   ├── mcp/        --> The MCP client.
│   └── ui/         --> The user interface code source
│   └── docs/       --> The documentation code source
├── tests/      --> The tests
└── notebooks/  --> Example and demo notebooks
```

## System Requirements

Install [just](https://just.systems) to run project-specific commands. You will also need to install [jq](https://stedolan.github.io/jq/download/) to parse JSON responses. You will need [uv](https://docs.astral.sh/uv/getting-started/installation/) to install python requirements

## Environment Variables

At a minimum, the project needs the following API key to be set perform LLM based metrics:

```bash
export OPENAI_API_KEY="Your secret key"
```

### Recommended: Hugging Face Token

For downloading datasets from Hugging Face (used during database seeding), it's recommended to set a Hugging Face token:

```bash
export HF_TOKEN="Your Hugging Face token"
```

You can create a token at [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens). While not strictly required, having a token provides:

- Higher rate limits for dataset downloads
- Access to gated datasets (if needed)
- Better reliability for API calls

The environement variables can also be defined in a `.env` file at the root of the project. See the `.env.example` file for an example.

All the project global settings and environmant variables are handled in `evalap/api/config.py`.

## Python Requirements

Install python requirements with:

```bash
just sync
```

This will also install pre-commit hooks.

## Development Setup

You can run EvalAP in two ways: using Docker Compose (recommended) or running services locally.

### Option 1: Docker Compose (Recommended)

This is the easiest way to get started with full hot reloading for all services.

#### Quick Start

```bash
docker compose -f compose.dev.yml up --build
```

This will:

- Build the development Docker image (includes dev dependencies like `watchdog`)
- Start PostgreSQL database
- Run Alembic migrations automatically
- Start all three services with hot reloading:
  - **Uvicorn API** on port 8000
  - **Runner** with file watching
  - **Streamlit UI** on port 8501

#### Access Your Services

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs or http://localhost:8000/redoc
- **Streamlit UI**: http://localhost:8501
- **PostgreSQL**: localhost:5432 (credentials: postgres/changeme)

#### Hot Reloading

Your code is live-mounted into the container. Any changes you make will automatically trigger reloads:

- **Edit API code** (e.g., `evalap/api/main.py`) → Uvicorn auto-reloads
- **Edit runner code** (e.g., `evalap/runners/tasks.py`) → Runner auto-restarts (you'll see `[Reloader]` messages)
- **Edit Streamlit code** (e.g., `evalap/ui/demo_streamlit/app.py`) → Streamlit prompts to rerun

#### Managing Docker Services

```bash
# View logs (all services)
docker compose -f compose.dev.yml logs -f

# View logs (specific service)
docker compose -f compose.dev.yml logs -f evalap_dev

# Enter the container
docker compose -f compose.dev.yml exec evalap_dev bash

# Inside the container, check process status
supervisorctl status

# Restart a specific process
supervisorctl restart uvicorn
supervisorctl restart runner
supervisorctl restart streamlit

# Stop services
docker compose -f compose.dev.yml down

# Rebuild after dependency changes
docker compose -f compose.dev.yml up --build
```

### Option 2: Local Development (Without Docker)

If you prefer to run services directly on your machine:

#### Database Setup

1. Launch the PostgreSQL database:

```bash
docker compose -f compose.dev.yml up -d postgres
```

2. Initialize/Update the database schema:

```bash
alembic -c evalap/api/alembic.ini upgrade head
```

3. If you modify the schema:

```bash
alembic -c evalap/api/alembic.ini revision --autogenerate -m "text explication"
alembic -c evalap/api/alembic.ini upgrade head
```

#### Run All Services

Launch the API, runner and streamlit together:

```bash
just run
# or explicitly: just run local
```

This will:

1. **Seed the database** with initial datasets from Hugging Face (if not already present):
   - **llm-values-CIVICS**: Cultural values evaluation dataset
   - **lmsys-toxic-chat**: Toxicity detection dataset
   - **DECCP**: Chinese censorship benchmark
2. Start all three services in parallel with colored output and hot reloading

Note: Having an `HF_TOKEN` set is recommended for better dataset download reliability.

#### Run Services Separately

If needed you can run each service individually:

**Launch the API:**

```bash
uvicorn evalap.api.main:app --reload
```

**Launch the runner:**

```bash
PYTHONPATH="." python -m evalap.runners
# To change the default logging level:
LOG_LEVEL="DEBUG" PYTHONPATH="." python -m evalap.runners
```

**Launch Streamlit:**

```bash
streamlit run evalap/ui/demo_streamlit/app.py --server.runOnSave true --server.headless=true
```

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

## Jupyter Tutorial

The `notebook/` directory contains examples of API usage.

## Adding new metrics

Each single metric should be defined in a file in `evalap/api/metrics/{metric_name}.py`.
The file should be self-contained, i.e contains the eventual prompt and settings related to the metric.
The metric should be decorated as following example to be registed as a known metric of EVALAP:

```python
from . import metric_registry

@metric_registry.register(
    name="metric_name", # the name that identified the metric
    description="Explain the metrics briefly"
    metric_type="llm",  # to be documented, not yet used
    require=["output", "output_true", "query"] # the fields that should be present in the dataset related to experiment under evaluation
)
def metric_name_metric(output:str, output_true:str, **kwargs) -> float:
    # ...
    # ...You code goes here
    # ...
    return score
    # or, if you want to store the intermediate generated observation by the metric (like a judge answer typically)
    #return score, observation
```

## Unit Tests

Tests can be found in api/tests.
To run unit tests, use :

    just test

## Install python package

    just publish

## use ruff

    just format

## Dependency Management

This project uses [Renovate](https://renovatebot.com/) for automated dependency management.

### What Renovate Does

- **Python dependencies**: Automatically updates the `uv.lock` file based on `pyproject.toml` constraints
- **Documentation dependencies**: Updates npm packages in the `docs/` folder
- **Docker dependencies**: Updates base images in Dockerfiles and docker-compose files
- **GitHub Actions**: Updates action versions in workflow files
- **Security updates**: Creates immediate PRs for vulnerability alerts
- **Lock file maintenance**: Monthly cleanup of lock files

### Configuration

The Renovate configuration is located in `.github/renovate.json5` and includes:

- **Scheduled updates**: Regular dependency checks throughout the week
  - Monday: Documentation npm dependencies
  - Tuesday: Docker dependencies
  - Wednesday: Python dev dependencies
  - Thursday: GitHub Actions
  - Monthly: Lock file maintenance (1st of month)
- **Grouped updates**: Dependencies are grouped to reduce PR noise
- **Version constraints**: Respects Python >=3.12 and Node >=18.0 requirements

### Managing Renovate PRs

1. **Review the changes**: Ensure updates don't break functionality
2. **Test locally**: Run `just test` after merging dependency updates
3. **Monitor schedules**:
   - Documentation npm deps: Monday 6am UTC
   - Docker deps: Tuesday 6am UTC
   - Python dev deps: Wednesday 6am UTC
   - GitHub Actions: Thursday 6am UTC
   - Lock file maintenance: 1st of month 6am UTC
   - Security updates: Immediate when vulnerabilities detected

For more configuration options, see the [Renovate documentation](https://docs.renovatebot.com/).
