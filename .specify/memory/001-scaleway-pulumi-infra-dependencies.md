# Memory: Scaleway Pulumi Infrastructure - Dependency Management

**Feature**: 001-scaleway-pulumi-infra
**Date**: 2025-11-08
**Topic**: Centralized dependency management using `uv`

## Key Decision

The EvalAP project uses **centralized dependency management** with a single top-level `pyproject.toml` and the `uv` package manager.

## Current Setup

**File**: `/Users/luis/Code/alliance/evalap/pyproject.toml`

### Existing Dependencies
- Python 3.12+
- FastAPI, SQLAlchemy, Alembic (API)
- Streamlit, Plotly (Frontend)
- pytest, pytest-asyncio (Testing)
- pydantic (already present)

### Dependency Groups
```toml
[dependency-groups]
dev = [
    "pre-commit>=4.3.0",
    "ruff>=0.13.0",
    "pytest-cov>=7.0.0",
    "ipykernel>=6.30.1",
    "watchdog>=6.0.0",
]
```

## Infrastructure Dependencies to Add

For the Scaleway Pulumi infrastructure feature, add to `[project.optional-dependencies]`:

```toml
[project.optional-dependencies]
# ... existing test dependencies ...
infra = [
    "pulumi>=3.206.0,<4.0.0",
    "pulumi-scaleway>=0.3.0,<1.0.0",
]
```

**Note**:
- `pydantic>=2.12.4` - Already in main dependencies
- `pytest>=9.0.0` - Already in test optional dependencies

## Installation Commands

**For developers working on infrastructure:**
```bash
# Install all dependencies including infrastructure
uv sync --all-extras

# Or install just infrastructure dependencies
uv sync --extra infra
```

**For running tests:**
```bash
# Run infrastructure tests
pytest infra/tests/unit/ -v
pytest infra/tests/integration/ -v

# Run with coverage
pytest infra/tests/ --cov=infra --cov-report=html
```

## Why Centralized?

1. **Single source of truth** - All project dependencies in one place
2. **Consistent versions** - No version conflicts between components
3. **Easier maintenance** - Update dependencies once for entire project
4. **Better tooling** - `uv` provides faster dependency resolution
5. **Cleaner structure** - No separate requirements.txt or infra/requirements.txt

## Tasks Affected

- **T004**: Add infrastructure dependencies to root `pyproject.toml`
- **T071-T072**: Integration tests use `uv sync` for dependency installation
- **T081-T082**: Full test suite runs with `uv sync` installed dependencies

## Related Files

- Root `pyproject.toml` - Central dependency configuration
- `infra/` - Infrastructure code (no separate requirements.txt)
- `.specify/templates/tasks-template.md` - Task generation template
- `specs/001-scaleway-pulumi-infra/tasks.md` - Generated tasks for this feature
