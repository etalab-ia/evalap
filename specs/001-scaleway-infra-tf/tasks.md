---
description: "Task list for Scaleway Infrastructure Setup with Pure Terraform"
---

# Tasks: Scaleway Infrastructure Setup with Pure Terraform

**Input**: Design documents from `/specs/001-scaleway-infra/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Infrastructure validation and integration tests included

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each infrastructure component.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Infrastructure**: `infra/` at repository root
- **OpenTofu**: Pure OpenTofu approach with separate environment directories
- **Modules**: Reusable OpenTofu modules in `infra/modules/`

### Critical Decision: Pure OpenTofu Approach

**Date**: 2025-11-07
**Status**: DECIDED - Use Pure OpenTofu

### Testing Results

After extensive testing of Terragrunt v0.93.3:

- ❌ **100% Failure Rate**: Every command (`validate`, `plan`, `apply`) crashes
- ❌ **Critical Error**: `panic: runtime error: invalid memory address or nil pointer dereference`
- ❌ **Production Risk**: Completely unreliable for infrastructure deployment

### OpenTofu Results

- ✅ **100% Success Rate**: All commands work perfectly
- ✅ **Proven Reliability**: Battle-tested and stable
- ✅ **Simpler Debugging**: Direct error messages
- ✅ **Better Security**: Easier credential handling

### Implementation Impact

All tasks updated to use pure OpenTofu approach:

- Removed Terragrunt configuration files
- Updated deployment scripts to use `tofu` commands
- Simplified project structure without complex include hierarchies
- Enhanced reliability and maintainability

**Conclusion**: Pure OpenTofu is the superior solution based on real-world testing results.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create infrastructure directory structure per implementation plan
- [x] T002 Initialize OpenTofu configuration files and modules
- [x] T003 [P] Configure HCL validation and formatting in pre-commit hooks
- [x] T004 [P] Set up Scaleway provider configuration and authentication
- [x] T005 Create documentation structure for infrastructure setup

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Setup Scaleway Object Storage backend for Terraform state
- [x] T007 Configure remote state locking and encryption
- [x] T008 Implement common provider configuration in \_common/
- [x] T009 Create base Terraform configuration and module structure
- [x] T010 Setup environment variable management and secret injection framework
- [x] T011 Configure GitHub Actions workflow infrastructure
- [x] T012 Create validation scripts for infrastructure compliance

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Deploy Staging Infrastructure (Priority: P1) 🎯 MVP

**Goal**: Deploy complete EvalAP infrastructure to staging environment for safe testing

**Independent Test**: Run staging deployment workflow and verify all services (documentation, runners, streamlit) are accessible via public endpoints with proper isolation from production

### Infrastructure Validation for User Story 1

- [x] T013 [P] [US1] Create staging environment validation test in tests/infra/test_staging_deployment.py
- [x] T014 [P] [US1] Create service isolation test in tests/infra/test_environment_isolation.py
- [x] T015 [P] [US1] Create deployment rollback test in tests/infra/test_staging_rollback.py

### Implementation for User Story 1

- [ ] T016 [US1] Create staging Terraform configuration in infra/staging/main.tf
- [ ] T017 [P] [US1] Implement staging container module in infra/staging/container/main.tf
- [ ] T018 [P] [US1] Create staging database module in infra/staging/database/main.tf
- [ ] T019 [P] [US1] Implement staging secrets module in infra/staging/secrets/main.tf
- [ ] T020 [P] [US1] Create staging monitoring module in infra/staging/monitoring/main.tf
- [ ] T021 [US1] Configure staging-specific variables in infra/staging/container/variables.tf
- [ ] T022 [US1] Set up staging database configuration in infra/staging/database/variables.tf
- [ ] T023 [US1] Implement staging secrets configuration in infra/staging/secrets/variables.tf
- [ ] T024 [US1] Configure staging monitoring in infra/staging/monitoring/variables.tf
- [ ] T025 [US1] Create staging outputs for service endpoints in infra/staging/container/outputs.tf
- [ ] T026 [US1] Add staging database connection outputs in infra/staging/database/outputs.tf
- [ ] T027 [US1] Implement staging deployment script in infra/scripts/deploy_staging.sh
- [ ] T028 [US1] Add staging validation and health checks in infra/scripts/validate_staging.sh

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Deploy Production with Redundancy (Priority: P1)

**Goal**: Deploy production infrastructure with high availability and 99.5% uptime

**Independent Test**: Deploy to production and simulate failures to verify automatic failover and service continuity within specified timeframes

### Infrastructure Validation for User Story 2

- [x] T029 [P] [US2] Create production redundancy test in tests/infra/test_production_redundancy.py
- [x] T030 [P] [US2] Create failover simulation test in tests/infra/test_production_failover.py
- [x] T031 [P] [US2] Create load balancing test in tests/infra/test_production_scaling.py

### Implementation for User Story 2

- [ ] T032 [US2] Create production Terraform configuration in infra/production/main.tf
- [ ] T033 [P] [US2] Implement production container module with redundancy in infra/production/container/main.tf
- [ ] T034 [P] [US2] Create production database with HA in infra/production/database/main.tf
- [ ] T035 [P] [US2] Implement production secrets with enhanced security in infra/production/secrets/main.tf
- [ ] T036 [P] [US2] Create production monitoring with comprehensive alerting in infra/production/monitoring/main.tf
- [ ] T037 [US2] Configure production scaling parameters in infra/production/container/variables.tf
- [ ] T038 [US2] Set up production database HA configuration in infra/production/database/variables.tf
- [ ] T039 [US2] Implement production security policies in infra/production/secrets/variables.tf
- [ ] T040 [US2] Configure production SLA monitoring in infra/production/monitoring/variables.tf
- [ ] T041 [US2] Create production service endpoints with load balancing in infra/production/container/outputs.tf
- [ ] T042 [US2] Add production database failover outputs in infra/production/database/outputs.tf
- [ ] T043 [US2] Implement production deployment script in infra/scripts/deploy_production.sh
- [ ] T044 [US2] Add production failover testing script in infra/scripts/test_production_failover.sh

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Manage Secrets Securely (Priority: P1)

**Goal**: Centralized secret management using Scaleway IAM Secret Manager with no hardcoded secrets

**Independent Test**: Configure secrets in IAM Secret Manager and verify infrastructure accesses them without any secrets stored in code or configuration files

### Infrastructure Validation for User Story 3

- [ ] T045 [P] [US3] Create secret management validation test in tests/infra/test_secret_management.py
- [ ] T046 [P] [US3] Create security audit test in tests/infra/test_security_compliance.py
- [ ] T047 [P] [US3] Create secret rotation test in tests/infra/test_secret_rotation.py

### Implementation for User Story 3

- [ ] T048 [US3] Create reusable secret manager module in infra/modules/secret-manager/main.tf
- [ ] T049 [P] [US3] Implement secret creation and management in infra/modules/secret-manager/variables.tf
- [ ] T050 [US3] Configure secret access policies in infra/modules/secret-manager/main.tf
- [ ] T051 [P] [US3] Create secret injection mechanism in infra/modules/secret-manager/main.tf
- [ ] T052 [US3] Implement secret rotation workflow in infra/modules/secret-manager/main.tf
- [ ] T053 [P] [US3] Update staging secrets to use centralized management in infra/staging/secrets/main.tf
- [ ] T054 [P] [US3] Update production secrets with enhanced security in infra/production/secrets/main.tf
- [ ] T055 [US3] Create secret management scripts in infra/scripts/manage_secrets.sh
- [ ] T056 [US3] Add security audit script in infra/scripts/audit_secrets.sh

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Configure PostgreSQL Database (Priority: P1)

**Goal**: Deploy managed PostgreSQL with automated backups and high availability

**Independent Test**: Deploy database stack, verify connectivity, test backup/restore procedures, and confirm HA failover capabilities

### Infrastructure Validation for User Story 4

- [ ] T057 [P] [US4] Create database connectivity test in tests/infra/test_database_connectivity.py
- [ ] T058 [P] [US4] Create backup and restore test in tests/infra/test_database_backup.py
- [ ] T059 [P] [US4] Create database HA failover test in tests/infra/test_database_ha.py

### Implementation for User Story 4

- [ ] T060 [US4] Create reusable PostgreSQL module in infra/modules/managed-postgresql/main.tf
- [ ] T061 [P] [US4] Implement database instance configuration in infra/modules/managed-postgresql/variables.tf
- [ ] T062 [US4] Configure automated backup system in infra/modules/managed-postgresql/main.tf
- [ ] T063 [P] [US4] Set up high availability configuration in infra/modules/managed-postgresql/main.tf
- [ ] T064 [US4] Implement database network security in infra/modules/managed-postgresql/main.tf
- [ ] T065 [P] [US4] Create database user management in infra/modules/managed-postgresql/main.tf
- [ ] T066 [US4] Configure staging database instance in infra/staging/database/main.tf
- [ ] T067 [P] [US4] Update production database with HA in infra/production/database/main.tf
- [ ] T068 [US4] Create database management scripts in infra/scripts/manage_database.sh
- [ ] T069 [US4] Add Alembic integration script in infra/scripts/run_migrations.sh
- [ ] T070 [P] [US4] Configure backup retention policy: 30 days daily, 90 days weekly, 1 year monthly in infra/modules/managed-postgresql/main.tf
- [ ] T071 [P] [US4] Implement backup lifecycle management and automated cleanup in infra/modules/managed-postgresql/main.tf
- [ ] T072 [US4] Create backup retention validation script in infra/scripts/validate_backup_retention.sh

---

## Phase 7: User Story 5 - Implement Zero-Downtime Deployments (Priority: P1)

**Goal**: Deploy application updates without service interruption with quick rollback capability

**Dependencies**: Requires User Story 6 (Container Services) to be complete - zero-downtime deployments operate on containerized services

**Independent Test**: Perform deployments during peak traffic and monitor for dropped requests, service interruption, or performance degradation

### Infrastructure Validation for User Story 5

- [ ] T073 [P] [US5] Create zero-downtime deployment test in tests/infra/test_zero_downtime_deployment.py
- [ ] T074 [P] [US5] Create rollback capability test in tests/infra/test_deployment_rollback.py
- [ ] T075 [P] [US5] Create deployment performance test in tests/infra/test_deployment_performance.py

### Implementation for User Story 5

- [ ] T076 [US5] Create rolling update strategy in infra/modules/serverless-container/main.tf
- [ ] T077 [P] [US5] Implement deployment health checks in infra/modules/serverless-container/main.tf
- [ ] T078 [US5] Configure traffic shifting during deployment in infra/modules/serverless-container/main.tf
- [ ] T079 [P] [US5] Create rollback mechanism in infra/modules/serverless-container/main.tf
- [ ] T080 [US5] Implement deployment monitoring in infra/modules/serverless-container/main.tf
- [ ] T081 [P] [US5] Update staging deployment with rolling updates in infra/staging/container/main.tf
- [ ] T082 [P] [US5] Configure production zero-downtime deployment in infra/production/container/main.tf
- [ ] T083 [US5] Create deployment orchestration script in infra/scripts/deploy_with_rolling_update.sh
- [ ] T084 [US5] Add rollback automation script in infra/scripts/emergency_rollback.sh

---

## Phase 8: User Story 6 - Containerize Services (Priority: P2)

**Goal**: Deploy three EvalAP services as Scaleway Serverless Containers with automatic scaling

**Independent Test**: Build and deploy container images for each service and verify they run correctly with proper scaling and health checks

### Infrastructure Validation for User Story 6

- [ ] T082 [P] [US6] Create container deployment test in tests/infra/test_container_deployment.py
- [ ] T083 [P] [US6] Create container scaling test in tests/infra/test_container_scaling.py
- [ ] T084 [P] [US6] Create container health check test in tests/infra/test_container_health.py

### Implementation for User Story 6

- [ ] T085 [US6] Create reusable serverless container module in infra/modules/serverless-container/main.tf
- [ ] T086 [P] [US6] Implement container configuration in infra/modules/serverless-container/variables.tf
- [ ] T087 [US6] Configure container scaling and health checks in infra/modules/serverless-container/main.tf
- [ ] T088 [P] [US6] Create container networking configuration in infra/modules/serverless-container/main.tf
- [ ] T089 [US6] Implement container environment variables in infra/modules/serverless-container/main.tf
- [ ] T090 [P] [US6] Configure documentation container in infra/staging/container/main.tf
- [ ] T091 [P] [US6] Configure runners container in infra/staging/container/main.tf
- [ ] T092 [P] [US6] Configure streamlit container in infra/staging/container/main.tf
- [ ] T093 [P] [US6] Update production containers with redundancy in infra/production/container/main.tf
- [ ] T094 [US6] Create container build and push script in infra/scripts/build_and_push_containers.sh

---

## Phase 9: User Story 7 - Monitor Infrastructure (Priority: P2)

**Goal**: Comprehensive monitoring and alerting for all infrastructure components

**Independent Test**: Deploy monitoring stack and verify that metrics, logs, and alerts are properly configured for all infrastructure components

### Infrastructure Validation for User Story 7

- [ ] T095 [P] [US7] Create monitoring configuration test in tests/infra/test_monitoring_setup.py
- [ ] T096 [P] [US7] Create alerting functionality test in tests/infra/test_alerting_system.py
- [ ] T097 [P] [US7] Create log aggregation test in tests/infra/test_log_aggregation.py

### Implementation for User Story 7

- [ ] T098 [US7] Create reusable Cockpit monitoring module in infra/modules/cockpit-monitoring/main.tf
- [ ] T099 [P] [US7] Implement monitoring configuration in infra/modules/cockpit-monitoring/variables.tf
- [ ] T100 [US7] Configure alert rules and thresholds in infra/modules/cockpit-monitoring/main.tf
- [ ] T101 [P] [US7] Create log aggregation setup in infra/modules/cockpit-monitoring/main.tf
- [ ] T102 [US7] Implement dashboard configuration in infra/modules/cockpit-monitoring/main.tf
- [ ] T103 [P] [US7] Configure staging monitoring in infra/staging/monitoring/main.tf
- [ ] T104 [P] [US7] Set up production comprehensive monitoring in infra/production/monitoring/main.tf
- [ ] T105 [US7] Create monitoring setup script in infra/scripts/setup_monitoring.sh
- [ ] T106 [US7] Add alert testing script in infra/scripts/test_alerts.sh

---

## Phase 10: User Story 8 - Automate via GitHub Actions (Priority: P2)

**Goal**: Trigger infrastructure deployments through GitHub Actions workflows

**Independent Test**: Trigger GitHub Actions workflows through pull requests and merges, verifying proper validation, deployment, and rollback capabilities

### Infrastructure Validation for User Story 8

- [ ] T107 [P] [US8] Create GitHub Actions validation test in tests/infra/test_github_workflows.py
- [ ] T108 [P] [US8] Create deployment workflow test in tests/infra/test_deployment_workflow.py
- [ ] T109 [P] [US8] Create rollback workflow test in tests/infra/test_rollback_workflow.py

### Implementation for User Story 8

- [ ] T110 [US8] Create infrastructure validation workflow in .github/workflows/infrastructure-validate.yml
- [ ] T111 [P] [US8] Implement staging deployment workflow in .github/workflows/infrastructure-staging.yml
- [ ] T112 [P] [US8] Create production deployment workflow in .github/workflows/infrastructure-production.yml
- [ ] T113 [US8] Configure workflow secrets and environment variables in .github/workflows/
- [ ] T114 [P] [US8] Implement workflow approval and review process in .github/workflows/
- [ ] T115 [US8] Create workflow rollback automation in .github/workflows/infrastructure-rollback.yml
- [ ] T116 [P] [US8] Add workflow notification system in .github/workflows/
- [ ] T117 [US8] Create workflow testing script in infra/scripts/test_workflows.sh

---

## Phase 12: Edge Case Handling & Resilience

**Purpose**: Handle specific edge cases and failure scenarios identified in specification

- [ ] T126 [P] Implement rate limiting and retry logic for Scaleway API calls in infra/modules/common/api-rate-limiter.tf
- [ ] T127 [P] Add connection failure handling and graceful degradation in deployment workflows in infra/scripts/handle_connection_failures.sh
- [ ] T128 [P] Implement container image pull failure recovery in infra/modules/serverless-container/main.tf
- [ ] T129 [P] Add concurrent deployment protection and locking in infra/scripts/prevent_concurrent_deployments.sh
- [ ] T130 [P] Implement Object Storage state backend failover in infra/modules/state-backend/main.tf
- [ ] T131 [P] Add secret rotation handling during active deployments in infra/modules/secret-manager/main.tf
- [ ] T132 [P] Implement database backup failure recovery and storage constraint handling in infra/modules/managed-postgresql/main.tf
- [ ] T133 [P] Add region-wide outage detection and manual intervention procedures in infra/docs/disaster-recovery.md
- [ ] T134 [FR-012] Audit all dependencies and infrastructure code to verify no third-party cloud services are used (except CI/CD platforms) in infra/scripts/audit_third_party_services.py

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T135 [P] Create comprehensive infrastructure documentation in infra/docs/
- [ ] T136 [P] Implement infrastructure cost monitoring and optimization
- [ ] T137 [P] Add comprehensive security scanning and compliance checks
- [ ] T138 [P] Create disaster recovery and backup verification procedures
- [ ] T139 [P] Implement infrastructure performance optimization
- [ ] T140 [P] Create troubleshooting and debugging guides
- [ ] T141 [P] Add infrastructure metrics collection and analysis
- [ ] T142 Run complete quickstart.md validation and documentation updates

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-10)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - May integrate with US1 but should be independently testable
- **User Story 3 (P1)**: Can start after Foundational - Critical for all other stories (security foundation)
- **User Story 4 (P1)**: Can start after Foundational - Required by US1, US2, US5, US6
- **User Story 5 (P1)**: Can start after Foundational - Depends on US6 (containers)
- **User Story 6 (P2)**: Can start after Foundational - Required by US1, US2, US5
- **User Story 7 (P2)**: Can start after Foundational - Monitors all other stories
- **User Story 8 (P2)**: Can start after Foundational - Automates all other stories

### Within Each User Story

- Tests MUST be written and validate infrastructure before implementation
- Core modules before environment-specific configurations
- Staging implementation before production (for validation)
- Core implementation before integration and automation
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, P1 stories can start in parallel
- All tests for a user story marked [P] can run in parallel
- Module implementations marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1 (Staging Infrastructure)

```bash
# Launch all tests for User Story 1 together:
Task: "Create staging environment validation test in infra/tests/test_staging_deployment.py"
Task: "Create service isolation test in infra/tests/test_environment_isolation.py"
Task: "Create deployment rollback test in infra/tests/test_staging_rollback.py"

# Launch all staging modules together:
Task: "Implement staging container module in infra/staging/container/main.tf"
Task: "Create staging database module in infra/staging/database/main.tf"
Task: "Implement staging secrets module in infra/staging/secrets/main.tf"
Task: "Create staging monitoring module in infra/staging/monitoring/main.tf"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Staging Infrastructure)
4. **STOP and VALIDATE**: Test staging deployment independently
5. Deploy/demo staging environment if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add remaining stories → Each adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Staging) + User Story 4 (Database)
   - Developer B: User Story 2 (Production) + User Story 3 (Security)
   - Developer C: User Story 6 (Containers) + User Story 5 (Deployments)
3. Later phases:
   - Developer A: User Story 7 (Monitoring) + User Story 8 (Automation)
   - Developer B: Integration and testing
   - Developer C: Documentation and polish

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently deployable and testable
- Infrastructure tests validate before implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Critical path: Foundational → Security → Database → Containers → Deployments → Automation
- Avoid: cross-story dependencies that break independence, hardcoded secrets, production changes without staging validation
