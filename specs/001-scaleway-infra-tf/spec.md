# Feature Specification: Scaleway Infrastructure Setup with Pure Terraform

**Feature Branch**: `001-scaleway-infra`  
**Created**: 2025-11-07  
**Status**: Draft  
**Input**: User description: "Create a new specification for **Scaleway Infrastructure Setup with Pure Terraform** that replaces the previous CDKTF approach..."

## Clarifications

### Session 2025-11-07

- Q: Container Image Source Strategy → A: Build and push images to Scaleway Container Registry during deployment
- Q: Database Migration Strategy → A: Alembic migrations triggered automatically during deployment
- Q: Zero-Downtime Deployment Strategy → A: Rolling updates with instance-by-instance replacement
- Q: Environment Promotion Strategy → A: Promote container images through environments, infrastructure stays separate
- Q: Backup Retention Policy → A: 30 days for daily backups, 90 days for weekly, 1 year for monthly

### Critical Decision: Terragrunt vs Pure Terraform

**Date**: 2025-11-07  
**Decision**: Adopt **Pure OpenTofu** approach instead of Terragrunt + Terraform

#### Why This Decision Was Made

After extensive testing and real-world validation, we discovered that **Terragrunt v0.93.3 is completely unusable**:

1. **100% Failure Rate**: Every Terragrunt command (`validate`, `plan`, `apply`) crashes with segmentation faults
2. **Critical Error**: `panic: runtime error: invalid memory address or nil pointer dereference`
3. **Production Risk**: Unreliable tool cannot be trusted for infrastructure deployment
4. **Complexity vs Reliability**: Terragrunt adds complexity without providing reliability

#### Pure Terraform Benefits (Proven in Practice)

- ✅ **100% Reliability**: All commands work perfectly
- ✅ **Simpler Debugging**: Direct error messages, no complex include chains
- ✅ **Faster Execution**: No include resolution overhead
- ✅ **Better Security**: Easier to secure credential handling
- ✅ **Easier Maintenance**: Fewer moving parts, clearer structure

#### Implementation Status

- ✅ **Staging Environment**: Fully implemented and tested with pure Terraform
- ✅ **Deployment Script**: Automated script with secure credential retrieval
- ✅ **Documentation**: Comprehensive guides and troubleshooting
- ✅ **Validation**: Real-world testing with actual Scaleway project

**Conclusion**: The theoretical benefits of Terragrunt (DRY configuration, hierarchical includes) are outweighed by its practical unreliability. Pure OpenTofu provides a robust, maintainable solution.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy Staging Infrastructure (Priority: P1)

As a developer, I want to deploy the complete EvalAP infrastructure to the staging environment so that I can safely test changes before they affect production.

**Why this priority**: Staging provides a safe testing environment that validates the entire infrastructure setup without risking production availability. This is the foundation for all other development work.

**Independent Test**: Can be fully tested by running the staging deployment workflow and verifying all services (documentation, runners, streamlit) are accessible via their public endpoints with proper isolation from production.

**Acceptance Scenarios**:

1. **Given** a clean Scaleway project, **When** I run the staging deployment workflow, **Then** all infrastructure components are provisioned in the staging environment
2. **Given** staging infrastructure is deployed, **When** I access the service endpoints, **Then** all services are functional and completely isolated from production
3. **Given** staging deployment fails, **When** I check the deployment logs, **Then** I can identify the specific failure point and rollback to the previous state

---

### User Story 2 - Deploy Production with Redundancy (Priority: P1)

As a system administrator, I want to deploy the EvalAP infrastructure to production with high availability and redundancy so that end users have reliable access to the application with 99.5% uptime.

**Why this priority**: Production availability is critical for end users. Redundancy ensures the system can handle failures without service interruption, meeting the SLA requirements.

**Independent Test**: Can be fully tested by deploying to production and simulating failures (container restarts, network issues) to verify automatic failover and service continuity within the specified timeframes.

**Acceptance Scenarios**:

1. **Given** production infrastructure is deployed, **When** a container instance fails, **Then** traffic is automatically rerouted within 10 seconds and a new instance starts within 30 seconds
2. **Given** production deployment, **When** I check service endpoints, **Then** minimum 2 instances are running per service with automatic load balancing
3. **Given** database failover scenario, **When** primary database fails, **Then** system automatically fails over to replica with minimal disruption

---

### User Story 3 - Manage Secrets Securely (Priority: P1)

As a security administrator, I want to manage all infrastructure secrets centrally using Scaleway IAM Secret Manager so that no secrets are hardcoded in configuration files and all sensitive data is properly secured.

**Why this priority**: Security is foundational - hardcoded secrets create major security vulnerabilities. Centralized secret management is required for compliance and best practices.

**Independent Test**: Can be fully tested by configuring secrets in IAM Secret Manager and verifying infrastructure can access them without any secrets being stored in code or configuration files.

**Acceptance Scenarios**:

1. **Given** infrastructure needs database credentials, **When** I deploy the stack, **Then** credentials are retrieved from IAM Secret Manager with no hardcoded values
2. **Given** secret rotation is required, **When** I update a secret in IAM Secret Manager, **Then** infrastructure can be updated to use the new secret without redeployment
3. **Given** security audit, **When** I scan all infrastructure code, **Then** no hardcoded secrets or sensitive data are found

---

### User Story 4 - Configure PostgreSQL Database (Priority: P1)

As a developer, I want to deploy a managed PostgreSQL database with automated backups and high availability so that application data is safely stored and protected against data loss.

**Why this priority**: Database is the core data storage component. Managed PostgreSQL with HA ensures data durability and availability, which is critical for application functionality.

**Independent Test**: Can be fully tested by deploying the database stack, verifying connectivity, testing backup/restore procedures, and confirming HA failover capabilities.

**Acceptance Scenarios**:

1. **Given** database infrastructure is deployed, **When** I connect to the database, **Then** I can successfully read/write data with proper authentication
2. **Given** database backup configuration, **When** I trigger a backup, **Then** automated backups are created and stored in Object Storage
3. **Given** HA configuration, **When** primary database fails, **Then** system automatically fails over to replica with data consistency

---

### User Story 5 - Implement Zero-Downtime Deployments (Priority: P1)

As a DevOps engineer, I want to deploy application updates without any service interruption so that users experience no downtime during deployments and can quickly rollback if issues occur.

**Why this priority**: Production uptime is critical. Zero-downtime deployments ensure continuous service availability while allowing for rapid iteration and quick rollback capabilities.

**Independent Test**: Can be fully tested by performing actual deployments during peak traffic and monitoring for any dropped requests, service interruption, or performance degradation.

**Acceptance Scenarios**:

1. **Given** a new application version is ready, **When** I deploy to production, **Then** no requests are dropped and deployment completes within 5 minutes
2. **Given** deployment encounters issues, **When** I trigger a rollback, **Then** system reverts to previous version within 2 minutes with no dropped requests
3. **Given** deployment in progress, **When** I monitor service metrics, **Then** response times remain under 2 seconds throughout the deployment

---

### User Story 6 - Containerize Services (Priority: P2)

As a developer, I want to deploy the three EvalAP services (documentation, runners, streamlit) as Scaleway Serverless Containers so that they can scale automatically and be managed efficiently.

**Why this priority**: Containerization provides consistent deployment environments and enables the serverless scaling capabilities required for the application architecture.

**Independent Test**: Can be fully tested by building and deploying container images for each service and verifying they run correctly with proper scaling and health checks.

**Acceptance Scenarios**:

1. **Given** container images are built, **When** I deploy the services, **Then** all three services start successfully and respond to health checks
2. **Given** traffic increases, **When** I monitor service scaling, **Then** containers automatically scale based on configured min/max limits
3. **Given** container failure, **When** a container becomes unhealthy, **Then** it's automatically replaced and traffic is rerouted

---

### User Story 7 - Monitor Infrastructure (Priority: P2)

As a system administrator, I want comprehensive monitoring and alerting for all infrastructure components so that I can proactively identify and resolve issues before they impact users.

**Why this priority**: Monitoring is essential for maintaining the 99.5% uptime SLA and ensuring rapid response to infrastructure issues.

**Independent Test**: Can be fully tested by deploying monitoring stack and verifying that metrics, logs, and alerts are properly configured for all infrastructure components.

**Acceptance Scenarios**:

1. **Given** monitoring is deployed, **When** I check the dashboard, **Then** all infrastructure metrics are visible and properly categorized
2. **Given** an infrastructure issue occurs, **When** the threshold is exceeded, **Then** appropriate alerts are sent to configured channels
3. **Given** log aggregation, **When** I search application logs, **Then** all service logs are centralized and searchable

---

### User Story 8 - Automate via GitHub Actions (Priority: P2)

As a developer, I want to trigger infrastructure deployments through GitHub Actions workflows so that I can manage infrastructure changes through the same Git-based workflow used for application code.

**Why this priority**: GitOps workflow provides consistency, auditability, and automation for infrastructure management, aligning with modern DevOps practices.

**Independent Test**: Can be fully tested by triggering GitHub Actions workflows through pull requests and merges, verifying proper validation, deployment, and rollback capabilities.

**Acceptance Scenarios**:

1. **Given** infrastructure changes are committed, **When** I open a pull request, **Then** validation workflow runs and checks the configuration
2. **Given** pull request is merged, **When** deployment workflow triggers, **Then** infrastructure is deployed to the appropriate environment
3. **Given** deployment fails, **When** I check the workflow logs, **Then** I can identify the failure and trigger automatic rollback

---

### Edge Cases & Success Criteria

#### Network and API Issues

- **Edge Case**: Scaleway API rate limits exceeded during deployment
  - **Success Criteria**: Implement exponential backoff with 5 retry attempts; deployments succeed within 10 minutes of rate limit encounter
  - **Measurement**: Monitor API response codes and retry delays; log rate limit events

- **Edge Case**: Network connectivity issues between GitHub Actions and Scaleway
  - **Success Criteria**: Detect connection failures within 30 seconds; retry with 60-second timeout; fail gracefully after 3 attempts
  - **Measurement**: Track connection success rate and average retry time

- **Edge Case**: Container image pull failure during deployment
  - **Success Criteria**: Fall back to previous working image within 2 minutes; alert on pull failures; maintain service availability
  - **Measurement**: Monitor image pull success rate and fallback trigger time

#### Concurrency and State Management

- **Edge Case**: Concurrent deployments to the same environment
  - **Success Criteria**: Prevent concurrent deployments with state locking; queue subsequent deployments; notify users of queue position
  - **Measurement**: Track concurrent deployment attempts and average queue wait time

- **Edge Case**: Object Storage state backend becomes unavailable
  - **Success Criteria**: Detect unavailability within 15 seconds; switch to backup state location; complete deployment within 5 minutes of recovery
  - **Measurement**: Monitor state backend availability and failover success rate

#### Security and Secrets

- **Edge Case**: Secret rotation during active deployments
  - **Success Criteria**: Complete in-progress deployment with old secrets; apply new secrets on next deployment; zero service interruption
  - **Measurement**: Track secret rotation events and deployment continuity

#### Database and Storage

- **Edge Case**: Database backup fails due to storage constraints
  - **Success Criteria**: Detect backup failure within 1 minute; trigger cleanup of old backups; retry backup within 5 minutes
  - **Measurement**: Monitor backup success rate and storage utilization

- **Edge Case**: Region-wide Scaleway outages
  - **Success Criteria**: Detect outage within 30 seconds; switch to read-only mode; provide clear status communication; auto-recover on service restoration
  - **Measurement**: Track outage detection time and recovery automation success rate

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provision Scaleway Serverless Containers for documentation, runners, and streamlit services
- **FR-001.1**: System MUST build and push container images to Scaleway Container Registry during deployment
- **FR-002**: System MUST configure automatic scaling with minimum 2 instances per service in production
- **FR-003**: System MUST deploy Scaleway Managed PostgreSQL with automated backups and high availability
- **FR-003.1**: System MUST trigger Alembic migrations automatically during deployment
- **FR-003.2**: System MUST implement backup retention: 30 days daily, 90 days weekly, 1 year monthly
- **FR-004**: System MUST integrate with Scaleway IAM Secret Manager for all sensitive configuration
- **FR-005**: System MUST configure Scaleway Cockpit for monitoring, logging, and alerting
- **FR-006**: System MUST implement complete environment isolation between staging and production
- **FR-006.1**: System MUST promote container images through environments while keeping infrastructure separate
- **FR-007**: System MUST use Scaleway Object Storage for remote state management
- **FR-008**: System MUST support zero-downtime deployments with rolling updates strategy
- **FR-009**: System MUST provide automated rollback capability within 2 minutes
- **FR-010**: System MUST implement health checks for all services with automatic failover
- **FR-011**: System MUST use OpenTofu for infrastructure provisioning (Terragrunt was tested and found to be completely unreliable with 100% segfault rate)
- **FR-012**: System MUST use pure OpenTofu approach without complex include systems for reliability and maintainability
- **FR-013**: System MUST not use any third-party cloud services beyond Scaleway, except for CI/CD platforms which may be external to enable automated deployment workflows
- **FR-014**: System MUST support GitHub Actions workflows for validation and deployment
- **FR-015**: System MUST maintain 99.5% uptime for production environment
- **FR-016**: System MUST ensure no hardcoded secrets in any configuration files
- **FR-017**: System MUST implement proper IAM roles with least privilege access
- **FR-018**: System MUST support both manual and automated deployment triggers
- **FR-019**: System MUST provide comprehensive logging for all infrastructure operations
- **FR-020**: System MUST validate all configurations before applying changes

### Non-Functional Requirements

#### Performance Requirements

- **NFR-001**: Infrastructure provisioning MUST complete within 15 minutes for complete setup from scratch
- **NFR-002**: Zero-downtime deployments MUST complete within 5 minutes with no dropped requests
- **NFR-003**: Rollback operations MUST complete within 2 minutes with no service interruption
- **NFR-004**: Service response times MUST remain under 2 seconds during normal operations and deployments
- **NFR-005**: Failed container instances MUST restart automatically within 30 seconds
- **NFR-006**: Traffic MUST be rerouted within 10 seconds of container failure detection

#### Availability & Reliability Requirements

- **NFR-007**: Production environment MUST maintain 99.5% uptime excluding scheduled maintenance
- **NFR-008**: Database backups MUST achieve 99.9% success rate with automated retry logic
- **NFR-009**: System MUST support automatic failover for database and container instances
- **NFR-010**: Infrastructure MUST support graceful degradation during partial outages

#### Security Requirements

- **NFR-011**: All secrets MUST be stored in Scaleway IAM Secret Manager with encryption at rest
- **NFR-012**: Infrastructure MUST implement least privilege access for all components
- **NFR-013**: Security audits MUST find zero hardcoded secrets in configuration files
- **NFR-014**: Network traffic between components MUST be encrypted using TLS 1.2+
- **NFR-015**: Infrastructure MUST support automated security scanning and compliance checks

#### Scalability Requirements

- **NFR-016**: System MUST support automatic scaling based on configured min/max limits
- **NFR-017**: Container scaling MUST handle traffic spikes without manual intervention
- **NFR-018**: Infrastructure MUST support scale-to-zero capability for cost optimization
- **NFR-019**: System MUST maintain performance under 10x normal load conditions

#### Maintainability Requirements

- **NFR-020**: Infrastructure code MUST be version-controlled and auditable
- **NFR-021**: All infrastructure changes MUST be validated before deployment
- **NFR-022**: System MUST support comprehensive monitoring and alerting
- **NFR-023**: Documentation MUST be kept current with infrastructure changes
- **NFR-024**: System MUST support automated testing of infrastructure components

#### Compliance Requirements

- **NFR-025**: Infrastructure MUST comply with EU AI Act requirements for AI evaluation platforms
- **NFR-026**: System MUST support RGAA accessibility compliance for deployed services
- **NFR-027**: Infrastructure MUST use only open source solutions and avoid vendor lock-in
- **NFR-028**: System MUST support audit trail generation for all infrastructure operations
- **NFR-029**: Infrastructure MUST enable ProConnect integration for government deployments

### Key Entities *(include if feature involves data)*

- **Infrastructure Environment**: Represents staging or production deployment with isolated resources
- **Serverless Container**: Represents individual service deployments with scaling and health configurations
- **Database Instance**: Represents PostgreSQL deployment with backup and HA configurations
- **Secret**: Represents sensitive data stored in IAM Secret Manager with versioning
- **Monitoring Configuration**: Represents alert rules, dashboards, and log aggregation settings
- **Deployment State**: Represents Terraform state stored in Object Storage with locking
- **IAM Policy**: Represents access permissions for infrastructure components

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Infrastructure provisioning completes successfully on first try in 95% of attempts (excluding network timeouts and external API rate limits). Success measured as successful Terraform apply without manual intervention
- **SC-002**: Zero-downtime deployments complete within 5 minutes with no dropped requests and response times under 2 seconds. Response times measured by infrastructure health checks during deployment
- **SC-003**: Rollback operations complete within 2 minutes with no service interruption or data loss. Success measured by service availability and data consistency checks
- **SC-004**: Production environment maintains 99.5% uptime excluding scheduled maintenance. Uptime calculated as (total_time - downtime) / total_time where downtime = service_unavailability > 30 seconds
- **SC-005**: Failed container instances restart automatically within 30 seconds with traffic rerouted within 10 seconds
- **SC-006**: Database backups complete successfully with 99.9% success rate and can be restored within 10 minutes
- **SC-007**: Security audits find zero hardcoded secrets or sensitive data in infrastructure code
- **SC-008**: Infrastructure changes can be deployed through GitHub Actions with 90% first-time success rate
- **SC-009**: Monitoring alerts trigger within 30 seconds of threshold breaches with appropriate severity levels
- **SC-010**: Complete infrastructure can be reproduced from scratch within 15 minutes using automated workflows
