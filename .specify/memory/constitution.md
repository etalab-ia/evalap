<!-- Sync Impact Report: Constitution v2.1.0 (TDD Principle Addition)
- Version: 2.0.0 → 2.1.0 (MINOR: Added Principle VIII for Test-Driven Development)
- Added: Principle VIII (Test-Driven Development) with comprehensive TDD guidance
- Sections: Test Organization, Test Coverage Requirements, Mocking & Isolation, Test Execution, Assertion Patterns
- Rationale: Formalize existing TDD practices observed in tests/ directory structure
- Templates requiring updates: ✅ AGENTS.md (added TDD principle to quick reference and testing section)
- Follow-up: None
-->

# EvalAP Constitution

## Mandatory French Government AI Principles

These principles are NON-NEGOTIABLE and inherited from the ai-kit constitution for all French Government AI projects.

### M1. EU AI Act Compliance (NON-NEGOTIABLE)

EvalAP MUST comply with the EU Artificial Intelligence Act. As an evaluation platform for LLM models, EvalAP itself is not a high-risk AI system, but it enables evaluation of high-risk AI systems used in government services.

**EvalAP-Specific Responsibilities**:
- Provide evaluation frameworks for assessing high-risk AI systems (legal assistance, benefits eligibility, etc.)
- Enable bias detection and fairness testing for government AI deployments
- Document AI model limitations and known failure modes in evaluation results
- Support audit trail generation for AI decisions in government services

**References**:
- [EU AI Act Official Site](https://artificialintelligenceact.eu/)
- [AI Act Compliance Checker](https://artificialintelligenceact.eu/assessment/eu-ai-act-compliance-checker/)

### M2. RGAA Accessibility Compliance (NON-NEGOTIABLE)

EvalAP's UI MUST comply with RGAA 4 (Référentiel Général d'Amélioration de l'Accessibilité).

**Requirements**:
- All UI components MUST meet RGAA 4 criteria (106 accessibility criteria based on WCAG)
- Support assistive technologies (screen readers, keyboard navigation)
- Ensure device-agnostic UX: services MUST work on mobile, tablet, and desktop
- Include automated accessibility testing in CI/CD pipelines
- Maintain accessibility declarations as required by law

**Rationale**: Accessibility ensures digital services are usable by all citizens. RGAA compliance is both a legal obligation and a fundamental right.

### M3. Open Source & Digital Commons (NON-NEGOTIABLE)

EvalAP MUST remain open source and privilege open source solutions.

**Requirements**:
- All EvalAP code remains under MIT license (already compliant)
- Privilege open source dependencies and tools over proprietary alternatives
- Privilege sovereign (French/European) solutions when choosing external services
- Document code clearly to enable reuse by other government teams
- Contribute improvements back to upstream open source projects when possible

**Rationale**: Open source ensures technical autonomy, avoids vendor lock-in, enables cost-sharing across administrations, and ensures transparency of public solutions.

### M4. DSFR Design System Compliance

EvalAP's UI SHOULD comply with DSFR (Système de Design de l'État - https://www.systeme-de-design.gouv.fr/).

**Requirements**:
- Streamlit UI components SHOULD follow DSFR guidelines where applicable
- Ensure responsive design patterns (mobile-first approach)
- Maintain visual consistency with French Government digital services

**Note**: Streamlit's component library has limitations for full DSFR compliance; prioritize RGAA accessibility over strict DSFR adherence.

### M5. ProConnect Authentication Standard

EvalAP's authentication layer SHOULD support ProConnect (https://partenaires.proconnect.gouv.fr/) for government deployments.

**Requirements**:
- Document ProConnect integration requirements for deployers
- Support both development/testing and production ProConnect environments
- Provide guidance for session management and logout flows

**Note**: Current implementation uses API key authentication; ProConnect integration is recommended for future government deployments.

## Core Principles (EvalAP-Specific)

### I. API-First Design

EvalAP is fundamentally an API platform for LLM evaluation. Every feature MUST be exposed through REST endpoints before UI integration. The API is the contract; UI is a consumer of that contract.

- API endpoints define the feature boundary
- Pydantic schemas MUST validate all inputs/outputs
- FastAPI dependency injection for cross-cutting concerns (auth, DB, logging)
- HTTP status codes follow REST semantics (410 Gone for deleted resources, 400 for validation, 500 for server errors)

### II. Modular Architecture

Code organization reflects functional domains, not technical layers. Each domain (datasets, experiments, metrics, runners) is self-contained with clear boundaries.

- `evalap/api/` contains API layer (endpoints, schemas, CRUD)
- `evalap/runners/` handles async task execution via ZeroMQ
- `evalap/clients/` provides LLM client abstractions (OpenAI, Anthropic, Mistral, Albert)
- `evalap/ui/` contains Streamlit UI (read-only visualization)
- `evalap/scripts/` contains standalone executable scripts for batch operations
- Cross-module imports MUST go through public interfaces, not internal modules

### III. Metric Registry Pattern

Metrics are extensible plugins registered at runtime. New metrics MUST follow the decorator pattern and be self-contained.

- All metrics live in `evalap/api/metrics/{metric_name}.py`
- Each metric file is self-contained (includes prompts, settings, logic)
- Metrics MUST be decorated with `@metric_registry.register()` specifying name, description, type, and required fields
- Metrics MUST declare their input requirements (e.g., "output", "output_true", "query")
- Metrics MAY return either a float score or (score, observation) tuple for intermediate results

### IV. Async-Ready Execution

Long-running operations (experiments, evaluations) MUST be non-blocking. The runner processes tasks asynchronously via ZeroMQ message passing.

- API endpoints dispatch tasks to the runner, returning immediately
- Runner processes tasks in background with status tracking
- Experiments track completion status: pending → running → finished/failure
- Results are persisted to PostgreSQL for later retrieval
- UI polls for status updates; no blocking waits

### V. Observability & Logging

All components MUST emit structured logs for debugging and monitoring. Logging is mandatory for task execution, API requests, and error conditions.

- Use `evalap.logger` for all logging
- Log at appropriate levels: DEBUG for detailed flow, INFO for milestones, WARNING for recoverable issues, ERROR for failures
- Include context (user ID, experiment ID, metric name) in log messages
- Environmental impact metrics (energy, GWP) MUST be computed and logged

### VI. Semantic Versioning & Breaking Changes

The project follows MAJOR.MINOR.PATCH versioning. Breaking changes MUST be documented and justified.

- MAJOR: Incompatible API changes, schema removals, endpoint deprecations
- MINOR: New features, new metrics, backward-compatible enhancements
- PATCH: Bug fixes, documentation, non-breaking improvements
- Schema changes MUST be managed via Alembic migrations
- Deprecated endpoints MUST be marked and given a sunset period

### VII. Notebook Support & Documentation

Jupyter notebooks serve as executable documentation and tutorials for API usage. Notebooks are first-class artifacts in the project.

- All notebooks live in `notebooks/` directory
- Notebooks MUST demonstrate real API usage with working examples
- Notebooks MUST use public API endpoints (not internal modules)
- Notebooks SHOULD include explanatory markdown cells describing concepts
- Notebooks MAY be excluded from linting via Ruff configuration
- Demo notebooks MUST be kept up-to-date with API changes
- Notebooks are valuable for onboarding and feature discovery

### VIII. Test-Driven Development (TDD)

Tests are mandatory and MUST be written alongside or before implementation. Testing is not optional; it is a core development practice.

**Test Organization**:
- All tests live in `tests/` directory mirroring source structure (e.g., `tests/endpoints/` mirrors `evalap/api/endpoints.py`)
- Base test classes (e.g., `TestApi`) MUST define setup/teardown methods for test isolation
- Test fixtures MUST be defined in `tests/conftest.py` with appropriate scoping (session, module, function)
- Fixtures MUST handle resource lifecycle: setup, yield, teardown

**Test Coverage Requirements**:
- Unit tests MUST cover individual functions and business logic
- Integration tests MUST cover API contracts and inter-service communication
- Parametrized tests MUST be used for testing multiple scenarios (use `@pytest.mark.parametrize`)
- Critical paths MUST have high coverage (API endpoints, CRUD operations, metrics)
- New features MUST include tests before or alongside implementation

**Mocking & Isolation**:
- External dependencies MUST be mocked using `unittest.mock` or `pytest` fixtures
- Tests MUST NOT depend on external services (APIs, databases) except test database
- Mocks MUST be scoped appropriately to avoid test pollution
- Integration tests MAY use real database via fixtures; unit tests MUST use mocks

**Test Execution**:
- All tests MUST pass before merge: `just test`
- Tests MUST be deterministic and not flaky
- Test failures MUST be investigated and fixed immediately
- Coverage reports SHOULD be generated: `just test-cov`

**Assertion Patterns**:
- Assertions MUST be clear and descriptive
- Helper functions (e.g., `log_and_assert`) SHOULD be used for common assertion patterns
- Test names MUST clearly describe what is being tested (e.g., `test_read_dataset_not_found`)
- Expected vs. actual values MUST be explicit in assertions

## Security & Privacy Standards

### Data Protection & Privacy

EvalAP MUST comply with GDPR and French data protection regulations.

**GDPR Compliance**:
- Implement data minimization: collect only necessary data for evaluation
- Provide clear privacy notices about data usage
- Enable user data access and deletion rights
- Document data processing activities and legal bases
- Implement data retention policies with automatic deletion

**AI-Specific Privacy**:
- Document what data is used for LLM model training vs. inference
- Implement mechanisms to prevent sensitive data leakage in evaluation outputs
- Provide transparency about evaluation methodologies
- Enable human review for high-stakes evaluation decisions
- Audit evaluation systems for bias and fairness regularly

### Security Requirements

**Authentication & Authorization**:
- Use secure authentication mechanisms (API keys, ProConnect for government deployments)
- Implement role-based access control (RBAC) for internal users
- Follow principle of least privilege for service accounts
- Rotate credentials and API keys regularly
- Use secure session management with appropriate timeouts

**Data Security**:
- Encrypt data at rest and in transit (TLS 1.3+)
- Use government-approved encryption standards
- Implement secure key management practices
- Sanitize and validate all user inputs
- Protect against common vulnerabilities (OWASP Top 10)

**AI Security**:
- Implement rate limiting to prevent abuse of evaluation endpoints
- Validate and sanitize prompts to prevent injection attacks
- Monitor for adversarial inputs and model manipulation attempts
- Document LLM model provenance and supply chain security

**Audit & Compliance**:
- Maintain comprehensive audit logs for security-relevant events
- Implement log retention per government requirements
- Enable security monitoring and alerting
- Conduct regular security assessments
- Document incident response procedures

### Transparency & Explainability

For AI-powered evaluation features:
- Provide clear explanations of how evaluation metrics work
- Document evaluation methodology and limitations
- Enable users to understand and challenge evaluation results
- Maintain transparency about data sources and model versions
- Disclose known failure modes and edge cases in metrics

## Technology Stack

### Required Technologies

- **API Framework**: FastAPI ~0.115.2 with Pydantic ~2.11.9 for validation
- **Database**: PostgreSQL with SQLAlchemy ~2.0.35 ORM and Alembic ~1.13.3 for migrations
- **Async Task Queue**: ZeroMQ ~26.2.0 for message passing between API and runner
- **Web Server**: Uvicorn ~0.32.0 for ASGI serving
- **UI Framework**: Streamlit ~1.40.1 (read-only visualization only)
- **LLM Clients**: Requests ~2.32.3 for HTTP calls to OpenAI, Anthropic, Mistral, Albert APIs
- **Data Processing**: Pandas ~2.2.3, PyArrow ~19.0.1 for dataset handling
- **Evaluation Libraries**: DeepEval ~3.5.1, RAGAS ~0.2.14, RapidFuzz ~3.13.0
- **Process Management**: Supervisor ~4.2.5 for managing API, runner, and UI processes
- **Linting & Formatting**: Ruff for Python code quality

### Excluded Directories

The following directories are managed by external tools and MUST be excluded from linting, formatting, and pre-commit hooks:
- `.specify/` (Spec Kit templates and memory)
- `.windsurf/` (Windsurf IDE configuration)
- `.cursor/` (Cursor IDE configuration)
- `.claude/` (Claude Code agent artifacts)

## Development Workflow

### Code Quality Gates

- **Linting**: Ruff MUST pass with rules F, E, W, Q, B, I enabled
- **Formatting**: Code MUST be formatted with Ruff formatter (line length: 111 characters)
- **Pre-commit Hooks**: All hooks in `.pre-commit-config.yaml` MUST pass before commit
- **Tests**: All tests MUST pass; new features MUST include tests
- **Type Hints**: Python 3.12+ type hints MUST be used throughout

### Testing Requirements

- Unit tests live in `tests/` mirroring the source structure
- Integration tests MUST cover API contracts and inter-service communication
- Test fixtures defined in `tests/conftest.py`
- Run tests with `just test`
- Aim for high coverage on critical paths (API endpoints, CRUD operations, metrics)

### Database Migrations

- Schema changes MUST use Alembic migrations
- Migrations MUST be generated with `alembic revision --autogenerate -m "description"`
- Migrations MUST be applied before deployment with `alembic upgrade head`
- Never modify migration files after they've been committed

### Development Environment

- Use Docker Compose for consistent local development: `docker compose -f compose.dev.yml up --build`
- Services include PostgreSQL, API (Uvicorn), Runner, and Streamlit UI
- Hot reloading enabled for all services via file watching
- Use `just` commands for common tasks (sync, run, test, format, publish)

## Governance

### Constitution Authority

This constitution supersedes all other development practices and guidelines. When conflicts arise, this document takes precedence.

### Amendment Process

1. **Proposal**: Document the proposed change with rationale
2. **Review**: Discuss with team leads and get consensus
3. **Documentation**: Update this file with new version and amendment date
4. **Migration**: Provide guidance for existing code to comply
5. **Commit**: Include amendment details in commit message

### Compliance Verification

- All PRs MUST verify compliance with core principles
- Code reviews MUST check for principle violations
- Complexity MUST be justified in PR descriptions
- Use `.specify/` for runtime development guidance and task specifications

### Version History

- v1.0.0 (2025-10-24): Initial constitution from codebase analysis
- v1.1.0 (2025-10-24): Added Principle VII for notebook support and documentation
- v2.0.0 (2025-10-24): Integrated French Government AI principles from ai-kit constitution; added mandatory compliance sections (EU AI Act, RGAA, Open Source, DSFR, ProConnect); added Security & Privacy Standards
- v2.1.0 (2025-10-24): Added Principle VIII for Test-Driven Development (TDD) with comprehensive testing guidance

**Version**: 2.1.0 | **Ratified**: 2025-10-24 | **Last Amended**: 2025-10-24
