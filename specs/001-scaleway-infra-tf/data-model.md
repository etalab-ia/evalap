# Data Model: Scaleway Infrastructure Setup

**Date**: 2025-11-07  
**Purpose**: Infrastructure data entities and their relationships for Terragrunt + OpenTofu setup

## Infrastructure Entities

### Environment Configuration

**Entity**: Infrastructure Environment
- **Description**: Represents staging or production deployment with isolated resources
- **Attributes**:
  - `environment_name`: string (staging|production)
  - `scaleway_region`: string (fr-par)
  - `scaleway_zone`: string (fr-par-2)
  - `project_id`: string (Scaleway project identifier)
  - `organization_id`: string (Scaleway organization identifier)
  - `state_bucket`: string (Object Storage bucket for Terraform state)
  - `state_key`: string (Terraform state file path)
- **Relationships**:
  - Contains: Serverless Containers, Database Instance, Secret Manager, Monitoring Configuration
  - Uses: IAM Policies, Network Configuration
- **Validation Rules**:
  - Environment names must be unique across deployments
  - Production requires minimum redundancy settings
  - State bucket must be unique per environment

### Serverless Container Configuration

**Entity**: Serverless Container
- **Description**: Individual service deployments with scaling and health configurations
- **Attributes**:
  - `container_name`: string (documentation|runners|streamlit)
  - `image_name`: string (Container Registry image reference)
  - `min_scale`: integer (Minimum instances: 1 staging, 2 production)
  - `max_scale`: integer (Maximum instances for traffic handling)
  - `cpu_limit`: integer (CPU allocation per instance)
  - `memory_limit`: integer (Memory allocation per instance)
  - `environment_variables`: map (Runtime configuration)
  - `health_check_path`: string (Health check endpoint)
  - `health_check_interval`: integer (Health check frequency)
  - `timeout_seconds`: integer (Request timeout)
  - `privacy`: string (public|private)
- **Relationships**:
  - Belongs to: Infrastructure Environment
  - Uses: Container Registry Image, Secret Manager secrets
  - Monitored by: Monitoring Configuration
- **Validation Rules**:
  - Production min_scale must be >= 2 for redundancy
  - Health check path must return 200 status
  - Environment variables must not contain hardcoded secrets
  - Memory and CPU limits must be sufficient for application requirements

### Database Configuration

**Entity**: Database Instance
- **Description**: PostgreSQL deployment with backup and HA configurations
- **Attributes**:
  - `database_name`: string (evalap-staging|evalap-production)
  - `database_version`: string (PostgreSQL version)
  - `instance_type`: string (Scaleway instance size)
  - `storage_size`: integer (Storage in GB)
  - `backup_retention_days`: integer (30 daily, 90 weekly, 365 monthly)
  - `backup_region`: string (Backup storage region)
  - `high_availability`: boolean (true for production)
  - `network_type`: string (private|public)
  - `allowed_ips`: array (Network access restrictions)
- **Relationships**:
  - Belongs to: Infrastructure Environment
  - Used by: Serverless Containers
  - Backed up to: Object Storage
  - Monitored by: Monitoring Configuration
- **Validation Rules**:
  - Production must have high_availability = true
  - Backup retention must follow compliance policy
  - Network access must be restricted to authorized sources
  - Storage size must accommodate expected data growth

### Secret Management

**Entity**: Secret
- **Description**: Sensitive data stored in IAM Secret Manager with versioning
- **Attributes**:
  - `secret_name`: string (Unique secret identifier)
  - `secret_version`: integer (Version number for rotation)
  - `secret_type`: string (database_url|api_key|certificate)
  - `description`: string (Human-readable description)
  - `rotation_period_days`: integer (Automatic rotation interval)
  - `access_policy`: string (IAM policy for access control)
- **Relationships**:
  - Stored in: IAM Secret Manager
  - Used by: Serverless Containers, Database Instance
  - Managed by: Infrastructure Environment
- **Validation Rules**:
  - Secret names must follow naming conventions
  - No sensitive data in configuration files
  - Access policies must follow least privilege principle
  - Rotation periods must comply with security policies

### Monitoring Configuration

**Entity**: Monitoring Configuration
- **Description**: Alert rules, dashboards, and log aggregation settings
- **Attributes**:
  - `dashboard_name`: string (Monitoring dashboard identifier)
  - `alert_rules`: array (Alert configuration objects)
  - `log_retention_days`: integer (Log storage duration)
  - `metric_collection_interval`: integer (Metrics gathering frequency)
  - `notification_channels`: array (Alert delivery methods)
- **Alert Rule Attributes**:
  - `rule_name`: string (Unique alert identifier)
  - `metric_name`: string (Monitored metric)
  - `threshold_value`: number (Alert trigger value)
  - `comparison_operator`: string (>|<|>=|<=)
  - `evaluation_period_seconds`: integer (Time to evaluate threshold)
  - `severity_level`: string (critical|warning|info)
- **Relationships**:
  - Monitors: Serverless Containers, Database Instance
  - Sends alerts to: Notification Channels
  - Stores logs in: Object Storage
- **Validation Rules**:
  - Alert thresholds must align with SLA requirements
  - Critical alerts must have <30 second response time
  - Log retention must comply with audit requirements
  - All infrastructure components must be monitored

### Deployment State

**Entity**: Deployment State
- **Description**: Terraform state stored in Object Storage with locking
- **Attributes**:
  - `state_file_path`: string (Object Storage path)
  - `state_version`: integer (State file version)
  - `lock_id`: string (State lock identifier)
  - `last_modified`: timestamp (State update time)
  - `serial_number`: integer (State serial for consistency)
- **Relationships**:
  - Stored in: Object Storage
  - Managed by: Terragrunt
  - Represents: Infrastructure Environment state
- **Validation Rules**:
  - State files must be encrypted
  - Lock must be acquired before state changes
  - State version must be tracked for rollbacks
  - Access must be restricted to authorized users

### IAM Policy Configuration

**Entity**: IAM Policy
- **Description**: Access permissions for infrastructure components
- **Attributes**:
  - `policy_name`: string (Unique policy identifier)
  - `policy_rules`: array (Permission rule objects)
  - `principal_type`: string (application|user|service)
  - `principal_id`: string (Scaleway principal identifier)
- **Policy Rule Attributes**:
  - `permission_set`: string (Predefined permission set)
  - `resource_type`: string (Target resource type)
  - `resource_ids`: array (Specific resource identifiers)
  - `effect`: string (allow|deny)
- **Relationships**:
  - Applied to: Infrastructure components
  - Managed by: Infrastructure Environment
  - Controls access to: All infrastructure resources
- **Validation Rules**:
  - Policies must follow least privilege principle
  - No overly permissive rules allowed
  - Resource-specific permissions preferred
  - Regular policy audits required

## Environment-Specific Configurations

### Staging Environment

**Configuration**:
- `min_scale`: 1 (single instance acceptable)
- `high_availability`: false (downtime acceptable)
- `backup_retention`: 7 days (shorter retention)
- `monitoring_level`: basic (reduced alerting)
- `network_type`: public (simplified access)

### Production Environment

**Configuration**:
- `min_scale`: 2 (redundancy required)
- `high_availability`: true (HA required)
- `backup_retention`: 30/90/365 days (compliance requirements)
- `monitoring_level`: comprehensive (full observability)
- `network_type`: private (enhanced security)

## State Transitions

### Deployment Lifecycle

1. **Planning**: Terragrunt validate and plan generation
2. **Approval**: Manual or automated approval of changes
3. **Deployment**: OpenTofu apply with state locking
4. **Verification**: Health checks and monitoring validation
5. **Rollback** (if needed): State restoration and service rollback

### Container Scaling States

1. **Idle**: Scale to zero (non-production only)
2. **Starting**: Instance initialization
3. **Healthy**: Serving traffic normally
4. **Unhealthy**: Health check failures
5. **Terminating**: Instance shutdown
6. **Replacing**: New instance deployment

### Database States

1. **Creating**: Initial database provisioning
2. **Active**: Normal operation mode
3. **Backing Up**: Automated backup process
4. **Failing Over**: HA replica promotion
5. **Restoring**: Backup restoration process
6. **Maintenance**: Scheduled maintenance window

## Validation Rules Summary

### Security Rules

- No hardcoded secrets in any configuration
- All network access must be explicitly allowed
- IAM policies must follow least privilege
- Data encryption at rest and in transit required

### Performance Rules

- Response times < 2 seconds during deployment
- Container restart < 30 seconds
- Traffic reroute < 10 seconds on failure
- 99.5% uptime for production

### Compliance Rules

- Backup retention: 30/90/365 days
- Audit logs retained for required periods
- Data residency within EU/Scaleway
- Regular security assessments required

### Operational Rules

- Environment isolation strictly maintained
- State locking enforced for concurrent deployments
- Health checks required for all services
- Monitoring coverage for all infrastructure components

## Integration Points

### Application Integration

- Database connection strings from Secret Manager
- Container images from Container Registry
- Environment variables injected at runtime
- Health check endpoints for monitoring

### CI/CD Integration

- GitHub Actions workflows for deployment
- Automated testing before production
- Rollback procedures for failed deployments
- Deployment status notifications

### Monitoring Integration

- Scaleway Cockpit metrics collection
- Custom application metrics via endpoints
- Alert routing to notification channels
- Log aggregation and search capabilities

This data model provides the foundation for implementing the Terragrunt + OpenTofu infrastructure with proper separation of concerns, security controls, and operational requirements.
