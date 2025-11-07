# Implementation Plan: Scaleway Infrastructure Setup with Pure Terraform

**Branch**: `001-scaleway-infra` | **Date**: 2025-11-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-scaleway-infra/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Replace CDKTF infrastructure setup with **Pure Terraform** for simpler, more reliable IaC. Deploy EvalAP application services (documentation, runners, streamlit) to Scaleway Serverless Containers with managed PostgreSQL, secret management, and monitoring. Support staging and production environments with complete isolation, zero-downtime deployments, and 99.5% uptime SLA.

## Technical Context

**Language/Version**: HCL (Terraform Configuration Language) + Shell scripts  
**Primary Dependencies**: Terraform >= 1.0, Scaleway Terraform Provider >= 2.0  
**Storage**: Scaleway Object Storage (S3-compatible) for Terraform state  
**Testing**: Terraform validate, integration tests via GitHub Actions  
**Target Platform**: Scaleway cloud infrastructure (fr-par region)  
**Project Type**: Infrastructure as Code (declarative configuration)  
**Performance Goals**: <5min deployments, <2sec response times, 99.5% uptime  
**Constraints**: Zero hardcoded secrets, complete environment isolation, no third-party cloud services beyond Scaleway  
**Scale/Scope**: 3 services (documentation, runners, streamlit), 2 environments (staging/production), managed PostgreSQL with HA

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Mandatory French Government AI Principles

**M1. EU AI Act Compliance**: ✅ PASSED - Infrastructure enables evaluation of high-risk AI systems without being high-risk itself
**M2. RGAA Accessibility Compliance**: ✅ PASSED - Infrastructure supports UI accessibility requirements (Streamlit will handle RGAA compliance)
**M3. Open Source & Digital Commons**: ✅ PASSED - Using open source OpenTofu/Terragrunt, avoiding vendor lock-in
**M4. DSFR Design System Compliance**: ✅ PASSED - Infrastructure supports DSFR-compliant UI deployment
**M5. ProConnect Authentication Standard**: ✅ PASSED - Infrastructure enables ProConnect integration for government deployments

### ✅ Core Principles

**I. API-First Design**: ✅ PASSED - Infrastructure supports FastAPI backend deployment
**II. Modular Architecture**: ✅ PASSED - Terragrunt modules align with modular approach
**III. Metric Registry Pattern**: ✅ PASSED - Infrastructure supports existing metric plugin system
**IV. Async-Ready Execution**: ✅ PASSED - Infrastructure enables ZeroMQ runner deployment
**V. Observability & Logging**: ✅ PASSED - Scaleway Cockpit integration for monitoring
**VI. Semantic Versioning & Breaking Changes**: ✅ PASSED - Infrastructure supports versioned deployments
**VII. Notebook Support & Documentation**: ✅ PASSED - Infrastructure enables notebook-based workflows
**VIII. Test-Driven Development (TDD)**: ✅ PASSED - Infrastructure includes comprehensive testing strategy

### ✅ Security & Privacy Standards

**GDPR Compliance**: ✅ PASSED - Infrastructure supports data protection requirements
**Security Requirements**: ✅ PASSED - IAM Secret Manager, least privilege access, encryption
**AI Security**: ✅ PASSED - Rate limiting, input validation, monitoring capabilities
**Audit & Compliance**: ✅ PASSED - Comprehensive logging and audit trails

### ✅ Technology Stack

**Required Technologies**: ✅ PASSED - All supported (PostgreSQL, monitoring, etc.)
**Excluded Directories**: ✅ PASSED - Proper exclusions configured in pre-commit hooks

### ✅ Development Workflow

**Code Quality Gates**: ✅ PASSED - HCL validation, formatting checks
**Testing Requirements**: ✅ PASSED - Infrastructure testing strategy defined
**Database Migrations**: ✅ PASSED - Alembic integration planned
**Development Environment**: ✅ PASSED - Local development with Docker Compose supported

**GATE STATUS**: ✅ **PASSED** - Ready for Phase 0 research

### ✅ Post-Design Constitution Re-check

**Phase 1 Design Validation**: All design decisions continue to align with constitution requirements:

- **Open Source Compliance**: ✅ OpenTofu, Terragrunt, and Scaleway provider are all open source
- **Modular Architecture**: ✅ Terragrunt modules and hierarchical configuration support modularity
- **Security Standards**: ✅ IAM Secret Manager, least privilege access, and encryption implemented
- **API-First Support**: ✅ Infrastructure enables FastAPI deployment and scaling
- **Observability**: ✅ Scaleway Cockpit integration provides comprehensive monitoring
- **Testing Strategy**: ✅ Infrastructure validation and integration testing defined

**Final GATE STATUS**: ✅ **PASSED** - Ready for Phase 2 task generation

## Project Structure

### Documentation (this feature)

```text
specs/001-scaleway-infra/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
infra/
├── README.md                   # Terraform-only approach documentation
├── main.tf                     # Root provider configuration (optional)
├── modules/                    # Reusable Terraform modules
│   ├── container/              # Serverless containers
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── database/               # PostgreSQL
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── secret-manager/         # Secret Manager
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── monitoring/             # Cockpit monitoring
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── state-backend/          # S3 + DynamoDB for state
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── scaleway-provider/      # Provider configuration
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── staging/                    # Staging environment
│   ├── main.tf                 # Staging infrastructure
│   ├── variables.tf            # Staging variables
│   ├── terraform.tfvars        # Staging variable values
│   └── backend.tf              # Staging state configuration
├── production/                 # Production environment
│   ├── main.tf                 # Production infrastructure
│   ├── variables.tf            # Production variables
│   ├── terraform.tfvars        # Production variable values
│   └── backend.tf              # Production state configuration
├── scripts/                    # Deployment and management scripts
│   ├── deploy_staging_terraform.sh    # Staging deployment
│   ├── deploy_production_terraform.sh # Production deployment
│   ├── manage_state.sh              # State management
│   ├── validate_compliance.sh       # Compliance validation
│   └── run_tests.sh                 # Test runner
├── docs/                       # Documentation
│   ├── architecture.md         # Architecture overview
│   ├── security.md             # Security practices
│   ├── deployment.md           # Deployment guide
│   └── troubleshooting.md      # Troubleshooting guide
└── tests/                      # Test suites
    ├── test_staging_deployment.py
    ├── test_production_deployment.py
    ├── test_environment_isolation.py
    └── conftest.py
```

**Structure Decision**: Terraform-only approach with flat directory structure and separate environment directories. This structure was chosen after discovering that Terragrunt v0.93.3 has 100% failure rate with segmentation faults, making it completely unusable for production infrastructure. Pure Terraform provides proven reliability with simpler debugging and maintenance.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
