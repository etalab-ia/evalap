# Tasks: Scaleway Infrastructure with Pulumi

**Input**: Design documents from `/specs/001-scaleway-pulumi-infra/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Tests are REQUIRED per spec.md (line 61: "User Scenarios & Testing _(mandatory)_") and plan.md (line 54: "✅ VIII. Test-Driven Development"). Tests are INCLUDED as explicit validation checkpoints after each major phase:
- Unit tests validate individual components (pytest with Pulumi testing framework)
- Integration tests validate full stack deployments
- Manual verification tests ensure infrastructure is accessible and functional
- Comprehensive test coverage required per FR-014 and constitution requirement VIII

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create infrastructure project structure per plan.md in `infra/` directory
- [ ] T002 [P] Initialize Pulumi project configuration in `infra/Pulumi.yaml`
- [ ] T003 [P] Create Python package structure with `__init__.py` files in `infra/components/`, `infra/stacks/`, `infra/config/`, `infra/lib/`, `infra/tests/`
- [ ] T004 [P] Add infrastructure dependencies to root `pyproject.toml` in `[project.optional-dependencies]` section: pulumi>=3.206.0, pulumi-scaleway>=0.3.0 (pydantic and pytest already present)
- [ ] T005 [P] Create environment configuration template in `.env.example` with Scaleway credentials placeholders
- [ ] T006 [P] Create `.gitignore` for infrastructure directory with Pulumi state and Python artifacts
- [ ] T007 Create stack configuration files: `Pulumi.dev.yaml`, `Pulumi.staging.yaml`, `Pulumi.production.yaml` in `infra/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Implement Scaleway provider configuration in `infra/project.py` with credential handling and region setup
- [ ] T009 [P] Create Pydantic configuration models in `infra/config/models.py` for StackConfiguration, ContainerConfig, DatabaseConfig, StorageConfig, NetworkConfig, MonitoringConfig
- [ ] T010 [P] Create Scaleway provider configuration in `infra/config/provider.py` with environment variable and config-based credential loading
- [ ] T011 [P] Implement Pulumi helper utilities in `infra/lib/pulumi_helpers.py` for common resource patterns and output handling
- [ ] T012 [P] Implement Scaleway-specific helpers in `infra/lib/scaleway_helpers.py` for naming conventions, tagging, and resource validation
- [ ] T013 [P] Create validation utilities in `infra/lib/validation.py` for infrastructure configuration validation
- [ ] T014 Create base component structure with abstract component class in `infra/components/__init__.py`
- [ ] T015 [P] Create test fixtures and mocks in `infra/tests/fixtures/scaleway_mocks.py` for unit testing
- [ ] T016 [P] Create test `__init__.py` files in `infra/tests/unit/` and `infra/tests/integration/`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

### Validation Tests for Foundational Phase

- [ ] T017 [P] Run unit tests for all configuration models in `infra/tests/unit/` to verify Pydantic validation
- [ ] T018 [P] Run unit tests for Pulumi helpers in `infra/tests/unit/test_pulumi_helpers.py` to verify utility functions
- [ ] T019 [P] Run unit tests for Scaleway helpers in `infra/tests/unit/test_scaleway_helpers.py` to verify naming and tagging
- [ ] T020 Verify provider configuration loads correctly with environment variables and config files
- [ ] T021 Verify all imports work correctly by running `python -c "from infra import *"` in infra directory

---

## Phase 3: User Story 1 - Deploy Managed Infrastructure (Priority: P1) 🎯 MVP

**Goal**: Enable infrastructure developers to deploy a complete application stack using Scaleway's managed services through Pulumi infrastructure as code, including serverless containers, managed databases, and object storage.

**Independent Test**: Deploy a simple web application with database backend using the infrastructure components and verify all components are provisioned and accessible through their respective endpoints.

### Implementation for User Story 1

- [ ] T022 [P] [US1] Create ServerlessContainer component in `infra/components/serverless_container.py` with container namespace, container definition, health checks, and endpoint exposure
- [ ] T023 [P] [US1] Create DatabaseInstance component in `infra/components/database.py` with PostgreSQL provisioning, backup configuration, and connection details
- [ ] T024 [P] [US1] Create ObjectStorageBucket component in `infra/components/object_storage.py` with bucket creation, versioning, and lifecycle rules
- [ ] T025 [US1] Implement development stack in `infra/stacks/dev.py` combining ServerlessContainer, DatabaseInstance, and ObjectStorageBucket with dev-appropriate resource limits
- [ ] T026 [US1] Export stack outputs in `infra/stacks/dev.py` for API endpoint, database host, and storage bucket name
- [ ] T027 [US1] Create `infra/__main__.py` entry point that instantiates the appropriate stack based on Pulumi stack selection
- [ ] T028 [US1] Add validation for container resource limits (CPU 100-4000 millicores, memory 128-8192 MB) in ServerlessContainer component
- [ ] T029 [US1] Add validation for database configuration (volume size 5-500 GB, backup retention 1-365 days) in DatabaseInstance component
- [ ] T030 [US1] Add validation for object storage bucket naming (globally unique, DNS-compliant) in ObjectStorageBucket component
- [ ] T031 [US1] Implement error handling and logging for infrastructure deployment failures in `infra/lib/pulumi_helpers.py`

### Validation Tests for User Story 1

- [ ] T032 [P] Run unit tests for ServerlessContainer component in `infra/tests/unit/test_serverless_container.py`
- [ ] T033 [P] Run unit tests for DatabaseInstance component in `infra/tests/unit/test_database.py`
- [ ] T034 [P] Run unit tests for ObjectStorageBucket component in `infra/tests/unit/test_object_storage.py`
- [ ] T035 Run `pulumi preview --stack dev` to verify infrastructure plan without errors
- [ ] T036 Run `pulumi up --stack dev --yes` to deploy development infrastructure
- [ ] T037 Verify API container endpoint is accessible: `curl $(pulumi stack output api_endpoint --stack dev)/health`
- [ ] T038 Verify database connection by connecting with psql or application test
- [ ] T039 Verify object storage bucket exists and is accessible via Scaleway console
- [ ] T040 Run `pulumi destroy --stack dev --yes` to clean up test deployment

**Checkpoint**: At this point, User Story 1 should be fully functional and validated - developers can deploy a complete application stack with containers, database, and storage.

---

## Phase 4: User Story 2 - Implement Sovereign State Management (Priority: P1)

**Goal**: Ensure all Pulumi infrastructure state is stored within Scaleway's ecosystem to maintain data sovereignty and enable secure collaboration among team members.

**Independent Test**: Configure Pulumi to use Scaleway Object Storage for state backend, perform infrastructure changes, and verify state files are properly stored, versioned, and locked for concurrent access.

### Implementation for User Story 2

- [ ] T041 [P] [US2] Create state backend component in `infra/components/state_backend.py` for Scaleway Object Storage configuration
- [ ] T042 [P] [US2] Implement state locking mechanism in `infra/components/state_backend.py` using Scaleway Managed PostgreSQL
- [ ] T043 [US2] Create state management documentation in `infra/docs/state_management.md` with backend setup instructions
- [ ] T044 [US2] Implement state backup configuration in `infra/components/state_backend.py` with versioning and retention policies
- [ ] T045 [US2] Add state validation utilities in `infra/lib/validation.py` to verify state integrity and consistency
- [ ] T046 [US2] Create state recovery procedures documentation in `infra/docs/state_management.md` for rollback scenarios
- [ ] T047 [US2] Implement concurrent deployment handling with state locking in `infra/lib/pulumi_helpers.py`
- [ ] T048 [US2] Add state monitoring and alerting configuration in `infra/components/monitoring.py` for state backend health

### Validation Tests for User Story 2

- [ ] T049 [P] Run unit tests for state backend component in `infra/tests/unit/test_state_backend.py`
- [ ] T050 Configure Scaleway Object Storage bucket for Pulumi state backend
- [ ] T051 Configure state locking with Scaleway Managed PostgreSQL
- [ ] T052 Deploy infrastructure to staging stack: `pulumi up --stack staging --yes`
- [ ] T053 Verify state file exists in Object Storage bucket with correct versioning
- [ ] T054 Verify state lock mechanism works by attempting concurrent deployments
- [ ] T055 Test state rollback by reverting to previous state version
- [ ] T056 Run `pulumi destroy --stack staging --yes` to clean up test deployment

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently and be validated - infrastructure can be deployed with sovereign state management in Scaleway Object Storage.

---

## Phase 5: User Story 3 - Configure Security and Access Control (Priority: P2)

**Goal**: Implement comprehensive security controls including credential management, network isolation, and principle of least privilege across all infrastructure components.

**Independent Test**: Deploy infrastructure with security configurations and verify that only authorized access is possible, all communications are properly isolated, and credentials are securely managed.

### Implementation for User Story 3

- [ ] T057 [P] [US3] Create Secret Manager component in `infra/components/secret_manager.py` for credential storage and rotation
- [ ] T058 [P] [US3] Create IAM policy component in `infra/components/iam_policy.py` for service-specific role definitions with least privilege
- [ ] T059 [P] [US3] Create PrivateNetwork component in `infra/components/private_network.py` for service isolation with subnet configuration
- [ ] T060 [US3] Integrate Secret Manager with ServerlessContainer component for environment variable injection
- [ ] T061 [US3] Integrate Secret Manager with DatabaseInstance component for credential management
- [ ] T062 [US3] Integrate PrivateNetwork with ServerlessContainer for network isolation
- [ ] T063 [US3] Integrate PrivateNetwork with DatabaseInstance for database access restriction
- [ ] T064 [US3] Implement IAM policy validation in `infra/lib/validation.py` to enforce least privilege principle
- [ ] T065 [US3] Create security configuration documentation in `infra/docs/security.md` with IAM, secret, and network setup
- [ ] T066 [US3] Add encryption configuration for data at rest and in transit in infrastructure components
- [ ] T067 [US3] Implement audit logging for all infrastructure changes in `infra/lib/pulumi_helpers.py`

### Validation Tests for User Story 3

- [ ] T068 [P] Run unit tests for Secret Manager component in `infra/tests/unit/test_secret_manager.py`
- [ ] T069 [P] Run unit tests for IAM policy component in `infra/tests/unit/test_iam_policy.py`
- [ ] T070 [P] Run unit tests for PrivateNetwork component in `infra/tests/unit/test_private_network.py`
- [ ] T071 Deploy infrastructure with security configurations: `pulumi up --stack staging --yes`
- [ ] T072 Verify secrets are stored in Scaleway Secret Manager and not in code
- [ ] T073 Verify IAM policies follow least privilege principle by checking Scaleway console
- [ ] T074 Verify private network is created and services are attached to it
- [ ] T075 Verify database is NOT accessible from public internet (only from private network)
- [ ] T076 Verify container can access database through private network connection
- [ ] T077 Test credential rotation by updating secrets and verifying services still work
- [ ] T078 Run `pulumi destroy --stack staging --yes` to clean up test deployment

**Checkpoint**: All user stories 1, 2, and 3 should now be independently functional and validated - infrastructure is deployed with complete security controls.

---

## Phase 6: User Story 4 - Set Up Monitoring and Observability (Priority: P3)

**Goal**: Provide comprehensive monitoring and alerting to ensure infrastructure reliability, performance optimization, and rapid issue detection.

**Independent Test**: Deploy monitoring configurations and verify that metrics, logs, and alerts are properly collected and accessible through Cockpit.

### Implementation for User Story 4

- [ ] T046 [P] [US4] Create Cockpit monitoring component in `infra/components/monitoring.py` for metrics and log collection
- [ ] T047 [P] [US4] Create alert channel configuration in `infra/components/monitoring.py` for email and webhook notifications
- [ ] T048 [P] [US4] Create metric rule definitions in `infra/components/monitoring.py` for CPU, memory, and response time thresholds
- [ ] T049 [US4] Integrate Cockpit monitoring with ServerlessContainer for application metrics
- [ ] T050 [US4] Integrate Cockpit monitoring with DatabaseInstance for database performance metrics
- [ ] T051 [US4] Integrate Cockpit monitoring with ObjectStorageBucket for storage metrics
- [ ] T052 [US4] Create dashboard configuration in `infra/components/monitoring.py` for operational views
- [ ] T053 [US4] Implement log aggregation and structured logging in `infra/lib/pulumi_helpers.py`
- [ ] T054 [US4] Create monitoring documentation in `infra/docs/monitoring.md` with dashboard and alert setup
- [ ] T055 [US4] Add health check configuration for all infrastructure components in monitoring component

### Validation Tests for User Story 4

- [ ] T056 [P] Run unit tests for Cockpit monitoring component in `infra/tests/unit/test_monitoring.py`
- [ ] T057 Deploy infrastructure with monitoring enabled: `pulumi up --stack staging --yes`
- [ ] T058 Verify Cockpit dashboard displays metrics for all infrastructure components
- [ ] T059 Verify logs are being collected and aggregated in Cockpit
- [ ] T060 Simulate container load and verify CPU/memory metrics are tracked
- [ ] T061 Simulate database query load and verify database metrics are tracked
- [ ] T062 Verify alert rules trigger when thresholds are exceeded
- [ ] T063 Verify alert notifications are sent to configured channels
- [ ] T064 Test dashboard displays all configured widgets and metrics
- [ ] T065 Run `pulumi destroy --stack staging --yes` to clean up test deployment

**Checkpoint**: All user stories 1-4 should now be complete and validated - infrastructure is fully deployed with comprehensive monitoring and observability.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and finalize the implementation

- [ ] T066 [P] Create architecture documentation in `infra/docs/architecture.md` with component diagrams and design patterns
- [ ] T067 [P] Create deployment procedures documentation in `infra/docs/deployment.md` with step-by-step deployment guide
- [ ] T068 [P] Create troubleshooting guide in `infra/docs/troubleshooting.md` with common issues and solutions
- [ ] T069 [P] Create unit tests for Pulumi helpers in `infra/tests/unit/test_pulumi_helpers.py`
- [ ] T070 [P] Create unit tests for Scaleway helpers in `infra/tests/unit/test_scaleway_helpers.py`
- [ ] T071 Create integration test for full stack deployment in `infra/tests/integration/test_full_stack.py` (use `uv sync` to install dependencies)
- [ ] T072 Create integration test for state management in `infra/tests/integration/test_state_management.py` (use `uv sync` to install dependencies)
- [ ] T073 [P] Add comprehensive error handling and retry logic for API failures in `infra/lib/pulumi_helpers.py`
- [ ] T074 [P] Implement exponential backoff for rate limit handling in `infra/lib/scaleway_helpers.py`
- [ ] T075 [P] Add timeout configurations for all Scaleway API calls in `infra/config/provider.py`
- [ ] T076 [P] Create staging stack configuration in `infra/stacks/staging.py` with production-like settings
- [ ] T077 [P] Create production stack configuration in `infra/stacks/production.py` with high availability and monitoring
- [ ] T078 Code cleanup and refactoring across all infrastructure modules
- [ ] T079 Run quickstart.md validation to ensure all documented procedures work correctly
- [ ] T080 Update project README with infrastructure setup instructions and links to documentation
- [ ] T081 Run full integration test suite: `pytest infra/tests/integration/ -v`
- [ ] T082 Run full unit test suite with coverage: `pytest infra/tests/unit/ --cov=infra --cov-report=html`
- [ ] T083 Final production deployment validation: `pulumi up --stack production --yes`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion - Core infrastructure deployment
- **User Story 2 (Phase 4)**: Depends on Foundational completion - Can run in parallel with US1 after Foundational
- **User Story 3 (Phase 5)**: Depends on Foundational completion - Can run in parallel with US1/US2 after Foundational
- **User Story 4 (Phase 6)**: Depends on Foundational completion - Can run in parallel with US1/US2/US3 after Foundational
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent of US1, can run in parallel
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1/US2 but independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1/US2/US3 but independently testable

### Within Each User Story

- Components before stacks
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002-T006)
- All Foundational tasks marked [P] can run in parallel within Phase 2 (T009-T013, T015-T016)
- All Foundational validation tests marked [P] can run in parallel (T017-T019)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All component implementations marked [P] within a story can run in parallel
- All validation tests marked [P] after each user story can run in parallel
- Different user stories can be worked on in parallel by different team members
- All unit tests marked [P] in Phase 7 can run in parallel (T069-T070, T073-T077)

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create ServerlessContainer component in infra/components/serverless_container.py"
Task: "Create DatabaseInstance component in infra/components/database.py"
Task: "Create ObjectStorageBucket component in infra/components/object_storage.py"

# Then sequentially:
Task: "Implement development stack in infra/stacks/dev.py"
Task: "Export stack outputs in infra/stacks/dev.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (7 tasks)
2. Complete Phase 2: Foundational (9 tasks) + Validation (5 tasks) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (10 tasks) + Validation (9 tasks)
4. **STOP and VALIDATE**: Run all validation tests after US1
   - Unit tests for all components
   - Deploy to dev stack
   - Verify endpoints are accessible
   - Verify database connectivity
   - Verify storage bucket exists
   - Clean up test deployment
5. Deploy/demo if ready

### Incremental Delivery with Validation

1. Complete Setup + Foundational + Validation → Foundation ready and tested
2. Add User Story 1 + Validation → Deploy and verify independently → MVP!
3. Add User Story 2 + Validation → Deploy and verify independently
4. Add User Story 3 + Validation → Deploy and verify independently
5. Add User Story 4 + Validation → Deploy and verify independently
6. Each story adds value without breaking previous stories
7. Run final validation suite in Phase 7

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational + Validation together
2. Once Foundational is validated:
   - Developer A: User Story 1 (Deploy Managed Infrastructure) + Validation
   - Developer B: User Story 2 (Sovereign State Management) + Validation
   - Developer C: User Story 3 (Security and Access Control) + Validation
3. Stories complete and validate independently
4. Developer D: User Story 4 (Monitoring and Observability) + Validation
5. All: Phase 7 Polish & Cross-Cutting Concerns + Final Validation

### Validation Checkpoints (When to Stop and Test)

- **After Foundational**: Run 5 validation tasks to verify foundation is solid
- **After User Story 1**: Run 9 validation tasks to verify infrastructure deployment works
- **After User Story 2**: Run 8 validation tasks to verify state management works
- **After User Story 3**: Run 11 validation tasks to verify security controls work
- **After User Story 4**: Run 10 validation tasks to verify monitoring works
- **Final Phase 7**: Run 3 final validation tasks (full test suite, production deployment)

---

## Task Summary

| Phase | Count | Purpose |
|-------|-------|---------|
| Phase 1: Setup | 7 | Project initialization |
| Phase 2: Foundational | 9 + 5 validation | Core infrastructure (BLOCKING) |
| Phase 3: User Story 1 (P1) | 10 + 9 validation | Deploy Managed Infrastructure |
| Phase 4: User Story 2 (P1) | 8 + 8 validation | Sovereign State Management |
| Phase 5: User Story 3 (P2) | 11 + 11 validation | Security and Access Control |
| Phase 6: User Story 4 (P3) | 10 + 10 validation | Monitoring and Observability |
| Phase 7: Polish | 18 | Documentation, tests, refinement |
| **TOTAL** | **116** | **Complete feature implementation with validation** |

### Task Distribution by User Story (Implementation + Validation)

- **User Story 1 (Deploy Managed Infrastructure)**: 10 implementation + 9 validation = 19 tasks
- **User Story 2 (Sovereign State Management)**: 8 implementation + 8 validation = 16 tasks
- **User Story 3 (Security and Access Control)**: 11 implementation + 11 validation = 22 tasks
- **User Story 4 (Monitoring and Observability)**: 10 implementation + 10 validation = 20 tasks

### Validation Checkpoints

- **After Foundational Phase**: 5 validation tasks (unit tests, import verification)
- **After User Story 1**: 9 validation tasks (unit tests, deployment, endpoint verification, cleanup)
- **After User Story 2**: 8 validation tasks (unit tests, state backend, locking, rollback)
- **After User Story 3**: 11 validation tasks (unit tests, security verification, isolation, credential rotation)
- **After User Story 4**: 10 validation tasks (unit tests, metrics, logs, alerts, dashboards)
- **Final Polish Phase**: 3 final validation tasks (full test suite, production deployment)

### Independent Test Criteria

- **US1**: Can deploy serverless container, managed database, and object storage; all components accessible via endpoints
- **US2**: Can configure Scaleway Object Storage backend; state files properly versioned and locked; concurrent deployments handled safely
- **US3**: Can deploy infrastructure with IAM policies, secrets, and private networks; only authorized access possible; communications isolated
- **US4**: Can collect metrics, logs, and alerts through Cockpit; dashboards display infrastructure health; alerts trigger on threshold violations

### Suggested MVP Scope

**Minimum Viable Product**: Complete Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (User Story 1)

This delivers the core capability: infrastructure developers can deploy a complete application stack (containers, database, storage) using Pulumi on Scaleway. This provides immediate value and enables all subsequent features.

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All paths are relative to repository root (`/Users/luis/Code/alliance/evalap`)
- Infrastructure code follows Python 3.12+ standards with type hints and Pydantic validation
- All components follow modular design pattern for reusability across environments
