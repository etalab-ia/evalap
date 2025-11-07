# Infrastructure Contracts: Scaleway Setup

**Date**: 2025-11-07  
**Purpose**: API contracts and interfaces for infrastructure management

## Container Deployment Contract

### Serverless Container Specification

```yaml
# Container deployment contract
container_spec:
  name: string
  image: string
  environment: string (staging|production)
  scaling:
    min_instances: integer
    max_instances: integer
  resources:
    cpu: integer (mCPU)
    memory: integer (MB)
  health:
    path: string
    interval: integer (seconds)
    timeout: integer (seconds)
  networking:
    privacy: string (public|private)
    domains: array[string] (optional)
  environment_variables:
    - name: string
      value: string
      secret: boolean (optional)
```

### Required Fields Validation

- `name`: Must match service name (documentation|runners|streamlit)
- `image`: Must reference valid Scaleway Container Registry image
- `environment`: Must be valid environment identifier
- `scaling.min_instances`: >=1 staging, >=2 production
- `health.path`: Must return HTTP 200 status
- `environment_variables`: No hardcoded secrets allowed

## Database Configuration Contract

### PostgreSQL Instance Specification

```yaml
# Database configuration contract
database_spec:
  name: string
  environment: string (staging|production)
  engine:
    version: string
    type: string
  storage:
    size_gb: integer
    type: string
  high_availability: boolean
  backup:
    retention_days: integer
    region: string
  network:
    type: string (private|public)
    allowed_ips: array[string]
  users:
    - name: string
      privileges: array[string]
```

### Required Fields Validation

- `name`: Must include environment suffix
- `high_availability`: true for production
- `backup.retention_days`: 7 staging, 30/90/365 production
- `network.allowed_ips`: Must restrict access
- `users`: At least one application user with appropriate privileges

## Secret Management Contract

### Secret Specification

```yaml
# Secret management contract
secret_spec:
  name: string
  type: string (database_url|api_key|certificate|generic)
  value: string (base64 encoded)
  environment: string (staging|production)
  rotation:
    enabled: boolean
    period_days: integer
  access_policy:
    principals: array[string]
    permissions: array[string]
```

### Required Fields Validation

- `name`: Must follow naming convention (env-service-type)
- `type`: Must be valid secret type
- `value`: Must be base64 encoded, not plaintext
- `access_policy.principals`: Must specify authorized principals
- `access_policy.permissions`: Must follow least privilege

## Monitoring Configuration Contract

### Alert Rule Specification

```yaml
# Monitoring alert contract
alert_rule_spec:
  name: string
  metric: string
  threshold:
    value: number
    operator: string (>|<|>=|<=)
    duration: integer (seconds)
  severity: string (critical|warning|info)
  notifications:
    channels: array[string]
    message_template: string
  conditions:
    query: string
    evaluation_window: integer (seconds)
```

### Required Fields Validation

- `name`: Must be unique within environment
- `threshold.duration`: Critical alerts <30 seconds
- `severity`: Must align with SLA impact
- `notifications.channels`: At least one valid channel
- `conditions.query`: Valid PromQL/MetricsQL query

## Deployment Workflow Contract

### Deployment Request Specification

```yaml
# Deployment workflow contract
deployment_request:
  environment: string (staging|production)
  services: array[string]
  version: string
  strategy: string (rolling|blue_green|canary)
  rollback:
    enabled: boolean
    timeout: integer (seconds)
  validation:
    health_checks: boolean
    smoke_tests: boolean
  notifications:
    slack: boolean
    email: boolean
```

### Deployment Response Specification

```yaml
# Deployment response contract
deployment_response:
  deployment_id: string
  status: string (pending|in_progress|completed|failed|rolled_back)
  start_time: timestamp
  end_time: timestamp (optional)
  services:
    - name: string
      status: string
      url: string (optional)
      health: string (healthy|unhealthy|unknown)
  rollback_info:
    available: boolean
    previous_version: string (optional)
  errors: array[string] (optional)
```

## State Management Contract

### Terraform State Specification

```yaml
# State management contract
state_spec:
  environment: string
  backend:
    type: string (s3)
    bucket: string
    key: string
    region: string
  locking:
    enabled: boolean
    timeout: integer (seconds)
  encryption:
    enabled: boolean
    algorithm: string
```

### Required Fields Validation

- `backend.bucket`: Must be unique per environment
- `locking.enabled`: Must be true for production
- `encryption.enabled`: Must be true for all environments
- `key`: Must follow path pattern (env/terraform.tfstate)

## Environment Configuration Contract

### Environment Specification

```yaml
# Environment configuration contract
environment_config:
  name: string (staging|production)
  scaleway:
    project_id: string
    organization_id: string
    region: string
    zone: string
  networking:
    vpc_id: string (optional)
    private_networking: boolean
  compliance:
    data_residency: string (EU)
    audit_logging: boolean
    encryption_required: boolean
```

### Required Fields Validation

- `name`: Must be valid environment identifier
- `scaleway.project_id`: Must be valid Scaleway project
- `scaleway.organization_id`: Must be valid Scaleway organization
- `compliance.data_residency`: Must be EU for government compliance

## Integration Contracts

### GitHub Actions Integration

```yaml
# GitHub Actions workflow contract
workflow_trigger:
  event: string (push|pull_request)
  branch: string
  environment: string
  validation_required: boolean
  approval_required: boolean
```

### Container Registry Integration

```yaml
# Container registry contract
image_spec:
  registry: string
  repository: string
  tag: string
  digest: string (optional)
  build_info:
    commit_sha: string
    build_time: timestamp
    builder: string
```

## Validation Rules Summary

### Security Validation

- All secrets must be referenced, not hardcoded
- Network access must be explicitly defined
- IAM policies must follow least privilege
- Encryption must be enabled for sensitive data

### Performance Validation

- Container scaling must meet redundancy requirements
- Health check intervals must be appropriate
- Alert thresholds must align with SLA
- Backup retention must meet compliance

### Compliance Validation

- Data residency must be within EU
- Audit logging must be enabled
- Encryption standards must be met
- Access controls must be documented

### Operational Validation

- Environment isolation must be maintained
- State locking must be configured
- Rollback procedures must be defined
- Monitoring coverage must be complete

## Error Handling Contracts

### Standard Error Response

```yaml
# Error response contract
error_response:
  code: string
  message: string
  details: object (optional)
  timestamp: timestamp
  request_id: string
```

### Error Codes

- `INFRA_001`: Invalid configuration
- `INFRA_002`: Resource limit exceeded
- `INFRA_003`: Permission denied
- `INFRA_004`: Resource not found
- `INFRA_005`: Deployment failed
- `INFRA_006`: Health check failed
- `INFRA_007`: Backup failed
- `INFRA_008`: State lock conflict

These contracts provide the interface definitions for implementing the Scaleway infrastructure with proper validation, error handling, and operational requirements.
