# Implementation Plan: Scaleway Infrastructure with Pulumi

**Branch**: `001-scaleway-pulumi-infra` | **Date**: 2025-11-08 | **Spec**: spec.md
**Input**: Feature specification from `/specs/001-scaleway-pulumi-infra/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deploy complete infrastructure stack on Scaleway using Pulumi with Python SDK, featuring serverless containers for applications, managed PostgreSQL for data persistence, object storage for state management, and comprehensive security through IAM and Secret Manager. Focus on sovereign state management within Scaleway ecosystem and cost optimization through managed services.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: Pulumi>=3.206.0,<4.0.0, pulumi-scaleway>=0.3.0,<1.0.0, pydantic>=2.12.4,<3.0.0, pytest>=9.0.0,<10.0.0
**Storage**: Scaleway Object Storage (state), Managed PostgreSQL (application data)
**Testing**: pytest with Pulumi testing framework, unit tests for infrastructure code
**Target Platform**: Scaleway cloud platform (infrastructure as code deployment)
**Project Type**: infrastructure (IaC modules and configurations)
**Performance Goals**: <10 minute deployment, <5 second API response, 99% uptime
**Constraints**: Scaleway-only services, cost optimization, managed services
**Scale/Scope**: Single team (<10 deployments/month), <1GB state storage, 2-3 concurrent deployments

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Analysis

**✅ M1. EU AI Act Compliance**: Infrastructure enables evaluation of high-risk AI systems without being a high-risk system itself. Provides audit trails and bias detection capabilities.

**✅ M2. RGAA Accessibility Compliance**: Not applicable to infrastructure code, but enables deployment of accessible UI components.

**✅ M3. Open Source & Digital Commons**: Uses open source Pulumi and Python, maintains MIT license, prioritizes sovereign Scaleway (French) services.

**✅ M4. DSFR Design System Compliance**: Infrastructure supports DSFR-compliant application deployment.

**✅ M5. ProConnect Authentication Standard**: Infrastructure enables ProConnect integration for government deployments.

**✅ I. API-First Design**: Infrastructure provisions API-first application components with proper endpoint exposure.

**✅ II. Modular Architecture**: Infrastructure follows modular design with reusable components for containers, databases, storage.

**✅ III. Metric Registry Pattern**: Infrastructure supports evaluation metrics deployment and execution.

**✅ IV. Async-Ready Execution**: Serverless containers provide async execution capabilities.

**✅ V. Observability & Logging**: Integrates with Cockpit for comprehensive monitoring and structured logging.

**✅ VI. Semantic Versioning & Breaking Changes**: Infrastructure as code enables proper versioning and change management.

**✅ VII. Notebook Support & Documentation**: Infrastructure enables notebook-based evaluation workflows.

**✅ VIII. Test-Driven Development**: Infrastructure code includes comprehensive test coverage with pytest and Pulumi testing framework.

### Technology Stack Compliance

**✅ Required Technologies**: Uses Python 3.12+, pytest, follows established patterns. Infrastructure provisions FastAPI, PostgreSQL, and other required services.

**✅ Development Workflow**: Infrastructure code follows Ruff linting, includes pre-commit hooks, proper test structure.

**✅ Security & Privacy**: Implements Scaleway IAM, Secret Manager, encryption at rest and in transit, follows GDPR compliance.

### GATE STATUS: ✅ PASSED (Phase 0) → ✅ PASSED (Phase 1)

All constitution requirements are satisfied. No violations requiring justification.

**Phase 1 Design Verification**:
- ✅ Infrastructure components follow modular architecture principle
- ✅ Type-safe configurations using Pydantic models
- ✅ Comprehensive test structure with unit and integration tests
- ✅ Security by design with IAM, Secret Manager, and network isolation
- ✅ Observability through Cockpit integration
- ✅ API-first design with OpenAPI contracts
- ✅ Sovereign Scaleway-only infrastructure maintained
- ✅ Cost optimization through managed services selection

## Project Structure

### Documentation (this feature)

```text
specs/001-scaleway-pulumi-infra/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
infra/                              # Infrastructure as code directory
├── Pulumi.yaml                     # Pulumi project configuration
├── Pulumi.dev.yaml                 # Development stack configuration
├── Pulumi.staging.yaml             # Staging stack configuration
├── Pulumi.production.yaml          # Production stack configuration
├── __main__.py                     # Main Pulumi program entry point
├── project.py                      # Pulumi project setup and provider configuration
├── components/                     # Reusable infrastructure components
│   ├── __init__.py
│   ├── serverless_container.py     # Serverless container component
│   ├── database.py                 # Managed PostgreSQL component
│   ├── object_storage.py           # Object storage component
│   ├── secret_manager.py           # Secret manager component
│   ├── private_network.py          # Private networking component
│   ├── monitoring.py               # Cockpit monitoring component
│   └── state_backend.py            # Pulumi state backend configuration
├── stacks/                         # Environment-specific stack configurations
│   ├── __init__.py
│   ├── dev.py                      # Development environment stack
│   ├── staging.py                  # Staging environment stack
│   └── production.py               # Production environment stack
├── config/                         # Configuration models and validation
│   ├── __init__.py
│   ├── models.py                   # Pydantic models for infrastructure config
│   └── provider.py                 # Scaleway provider configuration
├── lib/                            # Utility libraries and helpers
│   ├── __init__.py
│   ├── pulumi_helpers.py           # Common Pulumi utilities
│   ├── scaleway_helpers.py         # Scaleway-specific helpers
│   └── validation.py               # Infrastructure validation utilities
├── tests/                          # Infrastructure tests
│   ├── __init__.py
│   ├── unit/                       # Unit tests for components
│   │   ├── test_serverless_container.py
│   │   ├── test_database.py
│   │   ├── test_object_storage.py
│   │   └── test_secret_manager.py
│   ├── integration/                # Integration tests
│   │   ├── test_full_stack.py
│   │   └── test_state_management.py
│   └── fixtures/                   # Test fixtures and mocks
│       ├── __init__.py
│       └── scaleway_mocks.py
└── docs/                           # Infrastructure documentation
    ├── architecture.md             # Architecture overview
    ├── deployment.md               # Deployment procedures
    ├── state_management.md         # State backend documentation
    ├── security.md                 # Security configuration
    └── troubleshooting.md          # Common issues and solutions
```

**Structure Decision**: Infrastructure project using Pulumi with modular component design. Components in `infra/components/` provide reusable infrastructure building blocks. Stack-specific configurations in `infra/stacks/` enable environment management. Tests follow the established project structure with unit and integration tests. Configuration models in `infra/config/` provide type-safe infrastructure definitions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
