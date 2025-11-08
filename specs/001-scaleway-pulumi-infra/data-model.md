# Data Model: Scaleway Infrastructure with Pulumi

**Feature**: 001-scaleway-pulumi-infra | **Date**: 2025-11-08
**Phase**: 1 - Design & Contracts | **Status**: Complete

## Core Infrastructure Entities

### InfrastructureStack

Represents a complete deployment environment (dev/staging/production) with all associated resources.

**Fields**:
- `name`: str - Stack identifier (e.g., "dev", "staging", "production")
- `environment`: str - Environment type (development, staging, production)
- `region`: str - Scaleway region (e.g., "fr-par-2")
- `project_id`: str - Scaleway project ID
- `tags`: Dict[str, str] - Resource tags for cost allocation and identification

**Relationships**:
- Has many ServerlessContainer
- Has many DatabaseInstance
- Has many ObjectStorageBucket
- Has many Secret
- Has one PrivateNetwork
- Has one MonitoringConfig

**Validation Rules**:
- Name must match pattern: `^[a-z][a-z0-9-]*$`
- Environment must be one of: ["development", "staging", "production"]
- Region must be valid Scaleway region
- Project ID must be valid UUID

### ServerlessContainer

Represents a Scaleway Serverless Container for application deployment.

**Fields**:
- `name`: str - Container name
- `registryImage`: str - Container image URL (format: `rg.fr-par.scw.cloud/$NAMESPACE/$IMAGE`)
- `cpuLimit`: int - CPU limit in millicores (100-4000, e.g., 140 = 0.14 vCPU)
- `memoryLimit`: int - Memory limit in MB (128-8192, must match CPU allocation)
- `minScale`: int - Minimum number of instances (0-10)
- `maxScale`: int - Maximum number of instances (1-100)
- `timeout`: int - Request timeout in seconds (30-900, default 300)
- `environmentVariables`: Dict[str, str] - Runtime environment variables
- `secretEnvironmentVariables`: Dict[str, str] - Secret environment variables
- `healthChecks`: List[HealthCheckConfig] - Health check settings
- `maxConcurrency`: int - Maximum concurrent requests per instance
- `port`: int - Container port (default 8080)
- `protocol`: str - Protocol (http1 or h2c, default http1)
- `privacy`: str - Privacy setting (public or private, default public)
- `deploy`: bool - Whether to deploy the container (default true)

**Relationships**:
- Belongs to InfrastructureStack
- References Secret for credentials
- Attached to PrivateNetwork (optional, beta feature)

**Validation Rules**:
- CPU limit: 100-4000 millicores
- Memory limit: 128-8192 MB (must match CPU allocation per Scaleway limits)
- Min scale: 0-10
- Max scale: 1-100, and max_scale >= min_scale
- Timeout: 30-900 seconds
- Port: 1-65535
- Protocol: http1 or h2c
- Privacy: public or private

### DatabaseInstance

Represents a Scaleway Managed PostgreSQL instance.

**Fields**:
- `name`: str - Database instance name
- `engine`: str - Database engine (PostgreSQL, MySQL, etc.)
- `nodeType`: str - Instance size (e.g., "db-dev-s", "db-pro-m")
- `volumeSizeInGb`: int - Storage size in GB (5-500, only for sbs_5k/sbs_15k volume types)
- `volumeType`: str - Volume type (lssd, sbs_5k, sbs_15k)
- `backupScheduleRetention`: int - Backup retention period in days (1-365)
- `isHaCluster`: bool - Enable high availability with replica
- `userName`: str - Admin username (identifier for first user)
- `password`: str - Admin password (required for initial setup)
- `projectId`: str - Scaleway project ID
- `region`: str - Scaleway region
- `privateNetwork`: PrivateNetworkConfig - Private network attachment (optional)
- `tags`: Dict[str, str] - Resource tags

**Relationships**:
- Belongs to InfrastructureStack
- Has many DatabaseUser
- Has many DatabaseBackup
- References Secret for credentials

**Validation Rules**:
- Volume size: 5-500 GB (only for sbs_5k/sbs_15k)
- Volume type: lssd, sbs_5k, or sbs_15k
- Backup retention: 1-365 days
- Node type must be valid Scaleway offering
- User name: `^[a-z][a-z0-9_]*$`
- Password: required, minimum complexity
- isHaCluster: updates recreate the instance

### ObjectStorageBucket

Represents a Scaleway Object Storage bucket.

**Fields**:
- `name`: str - Bucket name (globally unique, DNS-compliant)
- `region`: str - Bucket region
- `projectId`: str - Scaleway project ID
- `versioning`: VersioningConfig - Versioning settings (enabled/suspended)
- `corsRules`: List[CorsRule] - CORS configuration rules
- `lifecycleRules`: List[LifecycleRule] - Object lifecycle policies
- `objectLockEnabled`: bool - Enable object lock (immutability)
- `tags`: Dict[str, str] - Bucket tags
- `forceDestroy`: bool - Force destroy even with objects (default false)

**Relationships**:
- Belongs to InfrastructureStack
- Has many StoredObject
- Has many LifecycleRule
- Has many CorsRule

**Validation Rules**:
- Name must be globally unique and DNS-compliant
- Region must be valid Scaleway region
- Versioning: enabled or suspended (cannot revert to unversioned)
- Storage class is per-object via lifecycle rules, not per-bucket
- Object lock is immutable once enabled

**Important Notes**:
- Storage class (STANDARD, GLACIER, ONEZONE_IA) is configured per-object or via lifecycle rules, not at bucket level
- Once versioning is enabled, bucket cannot return to unversioned state
- ACL attribute is deprecated; use BucketAcl resource instead

### Secret

Represents a secret stored in Scaleway Secret Manager.

**Fields**:
- `name`: str - Secret name (pattern: `^[a-z][a-z0-9-]*$`)
- `description`: str - Human-readable description
- `projectId`: str - Scaleway project ID
- `region`: str - Scaleway region
- `tags`: Dict[str, str] - Secret tags
- `versions`: List[SecretVersion] - Secret versions (immutable history)

**Relationships**:
- Belongs to InfrastructureStack
- Has many SecretVersion
- Referenced by ServerlessContainer
- Referenced by DatabaseInstance

**Validation Rules**:
- Name: `^[a-z][a-z0-9-]*$`
- Each version is immutable
- Versions are accessed via SecretVersion resource

**Important Notes**:
- Secret content is stored in SecretVersion resources, not directly in Secret
- Each update creates a new immutable version
- Secrets are encrypted at rest by Scaleway

### PrivateNetwork

Represents a Scaleway Private Network for service isolation.

**Fields**:
- `name`: str - Network name
- `projectId`: str - Scaleway project ID
- `region`: str - Scaleway region
- `subnets`: List[SubnetConfig] - Network subnets
- `tags`: Dict[str, str] - Network tags

**Relationships**:
- Belongs to InfrastructureStack
- Has many Subnet
- Has many NetworkAttachment

**Validation Rules**:
- CIDR must be valid private network range (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- Subnet CIDRs must be within network CIDR
- Subnet CIDRs must not overlap

**Important Notes**:
- Private networks enable secure inter-service communication
- Containers and databases can be attached to private networks
- Beta feature: VPC integration requires `activate_vpc_integration=true` on namespace

### MonitoringConfig

Represents monitoring and alerting configuration.

**Fields**:
- `enabled`: bool - Enable monitoring
- `alert_channels`: List[AlertChannel] - Notification channels
- `metric_rules`: List[MetricRule] - Metric alerting rules
- `log_rules`: List[LogRule] - Log monitoring rules
- `dashboard_configs`: List[DashboardConfig] - Custom dashboards

**Relationships**:
- Belongs to InfrastructureStack
- Has many AlertChannel
- Has many MetricRule
- Has many LogRule

**Validation Rules**:
- At least one alert channel if monitoring enabled
- Metric rules must have valid thresholds
- Log rules must have valid patterns

## Supporting Entities

### HealthCheckConfig

Configuration for container health checks.

**Fields**:
- `protocol`: str - Protocol (http, tcp)
- `path`: str - HTTP path (if protocol is http)
- `port`: int - Port number
- `interval_seconds`: int - Check interval
- `timeout_seconds`: int - Check timeout
- `healthy_threshold`: int - Consecutive successes to mark healthy
- `unhealthy_threshold`: int - Consecutive failures to mark unhealthy

**Validation Rules**:
- Protocol: ["http", "tcp"]
- Port: 1-65535
- Interval: 5-300 seconds
- Timeout: 1-60 seconds
- Thresholds: 1-10

### NetworkConfig

Network attachment configuration for services.

**Fields**:
- `private_network_id`: str - Private network ID
- `subnet_ids`: List[str] - Subnet IDs for attachment
- `public_ips`: List[str] - Public IP addresses (if any)
- `security_group_ids`: List[str] - Security group IDs

**Validation Rules**:
- Must attach to at least one subnet
- Security groups must exist in same VPC

### LifecycleRule

Object lifecycle rule for storage buckets.

**Fields**:
- `id`: str - Rule identifier
- `status`: str - Rule status (enabled, disabled)
- `filter`: LifecycleFilter - Object filter conditions
- `transitions`: List[StorageTransition] - Storage class transitions
- `expiration_days`: int - Object expiration in days

**Validation Rules**:
- Status: ["enabled", "disabled"]
- Transitions must be in chronological order
- Expiration: 1-3650 days

### MetricRule

Metric alerting rule configuration.

**Fields**:
- `name`: str - Rule name
- `metric_name`: str - Metric to monitor
- `threshold`: float - Alert threshold value
- `comparison`: str - Comparison operator (gt, lt, eq, gte, lte)
- `duration_seconds`: int - Alert duration
- `severity`: str - Alert severity (critical, warning, info)

**Validation Rules**:
- Comparison: ["gt", "lt", "eq", "gte", "lte"]
- Duration: 60-3600 seconds
- Severity: ["critical", "warning", "info"]

## State Management

### InfrastructureState

Represents Pulumi state stored in Object Storage.

**Fields**:
- `stack_name`: str - Stack identifier
- `state_version`: str - State version identifier
- `checkpoint_data`: str - Serialized state data
- `manifest_data`: str - Resource manifest
- `deployment_metadata`: Dict[str, Any] - Deployment information
- `locked`: bool - State lock status
- `locked_by`: str - Lock holder (if locked)
- `lock_timestamp`: datetime - Lock acquisition time

**Relationships**:
- Belongs to InfrastructureStack
- Has many StateSnapshot

**Validation Rules**:
- Stack name must match InfrastructureStack
- State version must be UUID
- Lock duration maximum: 1 hour

### StateSnapshot

Historical snapshot of infrastructure state.

**Fields**:
- `state_id`: str - Unique snapshot identifier
- `timestamp`: datetime - Snapshot creation time
- `state_data`: str - Complete state snapshot
- `resource_count`: int - Number of resources
- `deployment_id`: str - Associated deployment ID

**Relationships**:
- Belongs to InfrastructureState

**Validation Rules**:
- State ID must be UUID
- Resource count must be >= 0

## Configuration Models

### StackConfiguration

Complete configuration for an infrastructure stack.

**Fields**:
- `stack_info`: StackInfo - Basic stack information
- `containers`: List[ContainerConfig] - Container configurations
- `databases`: List[DatabaseConfig] - Database configurations
- `storage`: List[StorageConfig] - Storage configurations
- `networks`: NetworkConfig - Network configuration
- `monitoring`: MonitoringConfig - Monitoring configuration
- `secrets`: List[SecretConfig] - Secret configurations

**Validation Rules**:
- At least one container must be defined
- Database configuration required for production
- Monitoring required for production
- All names must be unique within stack

## Data Flow and State Transitions

### Stack Lifecycle

1. **Initialization**: Create InfrastructureStack with basic configuration
2. **Provisioning**: Create and configure all associated resources
3. **Active**: Resources running and serving traffic
4. **Update**: Modify resource configurations
5. **Rollback**: Revert to previous configuration
6. **Decommission**: Remove all resources and clean up state

### State Management Flow

1. **Lock Acquisition**: Acquire exclusive lock on InfrastructureState
2. **State Update**: Apply changes and update state data
3. **Checkpoint Creation**: Create state checkpoint in Object Storage
4. **Snapshot Creation**: Create historical snapshot for rollback
5. **Lock Release**: Release lock for next operation

### Resource Dependencies

- ServerlessContainer depends on PrivateNetwork, Secret
- DatabaseInstance depends on PrivateNetwork, Secret
- ObjectStorage depends on InfrastructureStack
- MonitoringConfig depends on all monitored resources
- InfrastructureState depends on all resources in stack

## Security Model

### Access Control

- InfrastructureStack: Project-level access
- ServerlessContainer: Service-level access
- DatabaseInstance: Database admin access
- Secret: Need-to-know access
- InfrastructureState: Operations team access

### Data Classification

- Public: Container images, monitoring metrics
- Internal: Resource configurations, network settings
- Confidential: Database credentials, API keys, secrets
- Restricted: Infrastructure state, audit logs

## Validation Rules Summary

All entities must follow these validation principles:
- Type safety through Pydantic models
- Referential integrity between related entities
- Business rule validation for domain-specific constraints
- Security validation for access control and data protection
- Operational validation for reliability and performance requirements
