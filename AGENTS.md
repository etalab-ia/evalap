# AGENTS.md - AI Agent Guidance for EvalAP Development

This document provides guidance for AI agents (Claude, Windsurf, Cursor, etc.) working on the EvalAP project. All agents MUST follow the EvalAP Constitution (`.specify/memory/constitution.md`) as the authoritative governance document.

## Quick Reference: Core Principles

### Mandatory French Government AI Principles (NON-NEGOTIABLE)

1. **EU AI Act Compliance** - Evaluate high-risk AI systems with bias detection and audit trails
2. **RGAA Accessibility** - All UI components MUST meet RGAA 4 criteria (WCAG standards)
3. **Open Source & Digital Commons** - Maintain MIT license, privilege open source solutions
4. **DSFR Design System** - Streamlit UI SHOULD follow French Government design patterns
5. **ProConnect Authentication** - Support government authentication for deployments

### EvalAP-Specific Principles

1. **API-First Design** - Features exposed via REST endpoints before UI integration
2. **Modular Architecture** - Code organized by functional domains (api, runners, clients, ui, scripts)
3. **Metric Registry Pattern** - Extensible metrics via `@metric_registry.register()` decorator
4. **Async-Ready Execution** - Non-blocking operations via ZeroMQ message passing
5. **Observability & Logging** - Structured logging mandatory using `evalap.logger`
6. **Semantic Versioning** - MAJOR.MINOR.PATCH with documented breaking changes
7. **Notebook Support** - Jupyter notebooks as first-class executable documentation
8. **Test-Driven Development** - Tests MUST be written alongside or before implementation; testing is mandatory

## Development Workflow

### Before Starting Work

- [ ] Read `.specify/memory/constitution.md` for authoritative governance
- [ ] Check `.specify/` directory for project specifications and task definitions
- [ ] Review `CONTRIBUTING.md` for development setup and conventions
- [ ] Verify you're on the correct branch (typically `main` or feature branch)

### Code Quality Gates (MUST PASS)

- **Linting**: Ruff with rules F, E, W, Q, B, I
- **Formatting**: Ruff formatter (line length: 111 characters)
- **Pre-commit Hooks**: All hooks in `.pre-commit-config.yaml` MUST pass
- **Tests**: New features MUST include tests; all tests MUST pass
- **Type Hints**: Python 3.12+ type hints MUST be used throughout

### Excluded Directories (DO NOT MODIFY)

These directories are managed by external tools and MUST be excluded from linting, formatting, and pre-commit hooks:

- `.specify/` - Spec Kit templates and memory (managed by /speckit commands)
- `.windsurf/` - Windsurf IDE configuration
- `.cursor/` - Cursor IDE configuration
- `.claude/` - Claude Code agent artifacts

**Action**: Never run formatters or linters on these directories. They are already configured to be excluded in `pyproject.toml` and `.pre-commit-config.yaml`.

## Common Tasks

### Adding a New Metric

**Location**: `evalap/api/metrics/{metric_name}.py`

**Requirements**:
- Self-contained file with metric logic, prompts, and settings
- Decorated with `@metric_registry.register()` specifying name, description, type, and required fields
- Declare input requirements (e.g., "output", "output_true", "query")
- Return either float score or (score, observation) tuple
- Include docstring explaining the metric

**Example**:
```python
from . import metric_registry

@metric_registry.register(
    name="my_metric",
    description="Brief description of what this metric evaluates",
    metric_type="llm",
    require=["output", "output_true"]
)
def my_metric(output: str, output_true: str, **kwargs) -> float:
    """Detailed docstring explaining the metric logic."""
    # Your implementation
    return score
```

### Adding an API Endpoint

**Location**: `evalap/api/endpoints.py`

**Requirements**:
- Use FastAPI router with appropriate HTTP method
- Define Pydantic schemas for request/response validation
- Use dependency injection for DB session and authentication
- Return appropriate HTTP status codes (410 for deleted resources, 400 for validation, 500 for errors)
- Include docstring and type hints
- Add corresponding CRUD operation in `evalap/api/crud.py` if needed

**Example**:
```python
@router.get("/resource/{id}", response_model=schemas.Resource, tags=["resources"])
def read_resource(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get a resource by ID."""
    resource = crud.get_resource(db, id)
    if resource is None:
        raise HTTPException(status_code=410, detail="Resource not found")
    return resource
```

### Adding a Database Migration

**When**: After modifying `evalap/api/models.py`

**Steps**:
1. Generate migration: `alembic -c evalap/api/alembic.ini revision --autogenerate -m "description"`
2. Review generated migration file in `evalap/api/alembic/versions/`
3. Apply migration: `alembic -c evalap/api/alembic.ini upgrade head`
4. Commit migration file with your changes

### Writing Tests (Principle VIII: Test-Driven Development)

**Location**: `tests/` (mirroring source structure)

**Test Organization**:
- Mirror source structure: `tests/endpoints/` for `evalap/api/endpoints.py`, etc.
- Use base test classes with setup/teardown: inherit from `TestApi` or similar
- Define fixtures in `tests/conftest.py` with appropriate scoping (session, module, function)
- Fixtures MUST handle lifecycle: setup, yield, teardown

**Requirements**:
- Unit tests MUST cover individual functions and business logic
- Integration tests MUST cover API contracts and inter-service communication
- Parametrized tests MUST be used for multiple scenarios: `@pytest.mark.parametrize`
- External dependencies MUST be mocked: `@patch` or pytest fixtures
- New features MUST include tests before or alongside implementation
- Run tests with `just test` and coverage with `just test-cov`
- Aim for high coverage on critical paths (API endpoints, CRUD, metrics)

**Mocking & Isolation**:
- Mock external services (LLM APIs, external databases) using `unittest.mock`
- Use pytest fixtures for test database and resource lifecycle
- Avoid test pollution: properly scope mocks and fixtures
- Integration tests MAY use real test database; unit tests MUST use mocks

**Example with Parametrization**:
```python
import pytest
from unittest.mock import patch

class TestResource(TestApi):
    @pytest.mark.parametrize("resource_data", [
        {"name": "test1", "description": "desc1"},
        {"name": "test2", "description": "desc2"},
    ])
    def test_create_resource(self, db: Session, resource_data):
        """Test creating resources with multiple scenarios."""
        result = crud.create_resource(db, resource_data)
        assert result.name == resource_data["name"]
        assert result.id is not None

    @patch("external_service.api_call")
    def test_with_mocked_dependency(self, mock_api):
        """Test with mocked external dependency."""
        mock_api.return_value = {"status": "success"}
        result = my_function()
        assert result["status"] == "success"
        mock_api.assert_called_once()
```

**Assertion Patterns**:
- Use clear, descriptive assertions
- Helper functions (e.g., `log_and_assert`) for common patterns
- Test names MUST describe what is tested: `test_read_dataset_not_found`
- Make expected vs. actual explicit

### Creating a Notebook

**Location**: `notebooks/` directory

**Requirements**:
- Demonstrate real API usage with working examples
- Use public API endpoints (not internal modules)
- Include explanatory markdown cells describing concepts
- Keep up-to-date with API changes
- Use descriptive filename (e.g., `tutorial_create_experiment.ipynb`)

**Best Practices**:
- Start with setup/imports cell
- Include environment variable setup if needed
- Show complete workflows from start to finish
- Include error handling examples
- Add comments explaining non-obvious steps

## Security & Privacy

### Data Handling

- Implement data minimization: collect only necessary data
- Enable user data access and deletion rights (GDPR)
- Document data processing activities
- Implement data retention policies with automatic deletion

### Authentication & Authorization

- Use secure authentication mechanisms (API keys, ProConnect for government)
- Implement role-based access control (RBAC) for internal users
- Follow principle of least privilege for service accounts
- Rotate credentials and API keys regularly

### Input Validation

- Sanitize and validate all user inputs
- Protect against common vulnerabilities (OWASP Top 10)
- Validate and sanitize prompts to prevent injection attacks
- Implement rate limiting for API endpoints

### Logging & Audit

- Use `evalap.logger` for all logging
- Include context (user ID, experiment ID, metric name) in log messages
- Maintain comprehensive audit logs for security-relevant events
- Log at appropriate levels: DEBUG, INFO, WARNING, ERROR

## Accessibility & Design

### RGAA Compliance (NON-NEGOTIABLE)

- All UI components MUST meet RGAA 4 criteria
- Support assistive technologies (screen readers, keyboard navigation)
- Ensure device-agnostic UX (mobile, tablet, desktop)
- Test UI components across device types

### DSFR Design System

- Streamlit UI components SHOULD follow DSFR guidelines where applicable
- Ensure responsive design patterns (mobile-first approach)
- Maintain visual consistency with French Government digital services

**Note**: Streamlit has limitations for full DSFR compliance; prioritize RGAA accessibility.

## Versioning & Breaking Changes

### Version Format

EvalAP follows MAJOR.MINOR.PATCH semantic versioning:

- **MAJOR**: Incompatible API changes, schema removals, endpoint deprecations
- **MINOR**: New features, new metrics, backward-compatible enhancements
- **PATCH**: Bug fixes, documentation, non-breaking improvements

### Breaking Changes

- MUST be documented in commit message and PR description
- MUST include migration guidance for users
- MUST be marked as deprecated before removal (when possible)
- MUST include rationale in PR

## PR & Commit Guidelines

### Commit Messages

Follow the format: `type: description`

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Build, dependencies, tooling

**Example**:
```
feat: add bias detection metric for high-risk AI evaluation

- Implement fairness testing across demographic groups
- Add bias report generation in evaluation results
- Include documentation and example notebook
- Follows Principle M1 (EU AI Act Compliance)
```

### Pull Requests

- **Title**: Clear, descriptive, follows commit message format
- **Description**: Explain what, why, and how
- **Scope**: Keep PRs focused and reviewable
- **Tests**: Include tests for new features
- **Documentation**: Update docs if needed
- **Constitution Check**: Verify compliance with core principles

**PR Template**:
```markdown
## What
Brief description of changes

## Why
Rationale and context

## How
Implementation approach

## Verification
How to test/verify changes

## Constitution Alignment
- [ ] Principle X: Explanation
- [ ] Principle Y: Explanation
```

## Useful Commands

```bash
# Development setup
just sync                    # Install dependencies and pre-commit hooks
just run                     # Run all services locally
just run local              # Alternative: run all services locally

# Code quality
just format                  # Format code with Ruff
just test                    # Run all tests
just test-cov              # Run tests with coverage

# Database
alembic -c evalap/api/alembic.ini revision --autogenerate -m "description"
alembic -c evalap/api/alembic.ini upgrade head

# Docker
docker compose -f compose.dev.yml up --build
docker compose -f compose.dev.yml logs -f
docker compose -f compose.dev.yml exec evalap_dev bash
```

## Resources

- **Constitution**: `.specify/memory/constitution.md`
- **Contributing Guide**: `CONTRIBUTING.md`
- **API Documentation**: http://localhost:8000/docs (when running locally)
- **Project Documentation**: https://evalap.etalab.gouv.fr/doc
- **EU AI Act**: https://artificialintelligenceact.eu/
- **RGAA Standards**: https://accessibilite.numerique.gouv.fr/
- **DSFR Design System**: https://www.systeme-de-design.gouv.fr/

## Questions & Escalation

When uncertain about implementation decisions:

1. **Check the Constitution** - `.specify/memory/constitution.md` is authoritative
2. **Review CONTRIBUTING.md** - Development conventions and setup
3. **Look at existing code** - Follow established patterns
4. **Ask in PR comments** - Request clarification from maintainers
5. **Escalate to team leads** - For governance or architecture questions

## Agent-Specific Notes

### Claude (via Claude Code)

- Access to `.specify/` directory for specifications and task definitions
- Use `/speckit` commands for specification-driven development
- Artifacts stored in `.claude/` are excluded from linting
- Follow constitution principles in all code generation

### Windsurf

- Configuration stored in `.windsurf/` (excluded from linting)
- Use Windsurf's code editing capabilities for refactoring
- Respect pre-commit hooks and code quality gates
- Reference constitution in commit messages

### Cursor

- Configuration stored in `.cursor/` (excluded from linting)
- Use Cursor's AI features for code generation and debugging
- Ensure generated code passes all quality gates
- Include constitution alignment in PR descriptions

---

**Last Updated**: 2025-10-24 | **Constitution Version**: 2.1.0

For questions or updates to this document, refer to the Constitution amendment process in `.specify/memory/constitution.md`.
