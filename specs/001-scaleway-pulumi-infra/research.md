# Research Report: Scaleway Infrastructure with Pulumi

**Feature**: 001-scaleway-pulumi-infra | **Date**: 2025-11-08
**Phase**: 0 - Outline & Research | **Status**: Complete

## Technology Decisions

### Pulumi vs Terraform vs CDKTF

**Decision**: Pulumi with Python SDK

**Rationale**: 
- Python SDK aligns with EvalAP's existing technology stack and team expertise
- Type-safe infrastructure definitions using Python type hints
- Better integration with existing Python tooling (pytest, ruff, etc.)
- Real programming language enables complex logic and abstractions
- Strong testing support with Pulumi's testing framework
- Python ecosystem for configuration management and validation

**Alternatives Considered**:
- Terraform: Requires learning HCL, weaker type safety, limited testing capabilities
- CDKTF: TypeScript primary, less mature than Pulumi, more complex setup

### Scaleway Provider Selection

**Decision**: pulumi-scaleway official provider (v1.36.0+)

**Rationale**:
- Official community-maintained provider with comprehensive Scaleway service coverage
- Active maintenance and support from Pulumiverse
- Native Python integration with Pulumi SDK
- Supports all required services:
  - **Compute**: Container, ContainerNamespace, Function, FunctionNamespace
  - **Database**: DatabaseInstance, Database, DatabaseUser, DatabaseBackup, DatabaseReadReplica
  - **Storage**: ObjectBucket, ObjectBucketPolicy, ObjectItem
  - **Networking**: VpcPrivateNetwork, VpcPublicGateway, VpcRoute
  - **Security**: Secret, SecretVersion, IamPolicy, IamApplication, IamApiKey
  - **Monitoring**: Cockpit, CockpitAlertManager, CockpitToken
  - **Additional**: DomainZone, DomainRecord, RegistryNamespace, and many more

**Alternatives Considered**:
- Scaleway API direct calls: Would require custom state management, losing IaC benefits
- Terraform Scaleway provider: Would require Terraform instead of Pulumi

### State Backend Strategy

**Decision**: Scaleway Object Storage with state locking

**Rationale**:
- Sovereign state management within Scaleway ecosystem
- Object Storage provides durable, versioned storage
- State locking via Scaleway Managed PostgreSQL for consistency
- Compliance with data residency requirements
- Cost-effective for small team usage (<1GB state)

**Alternatives Considered**:
- Pulumi Cloud: External service, violates Scaleway-only constraint
- Local state: No collaboration, single point of failure

## Architecture Patterns

### Component-Based Infrastructure

**Decision**: Modular components with reusable abstractions

**Rationale**:
- Enables infrastructure reuse across environments (dev/staging/production)
- Simplifies testing through isolated components
- Follows EvalAP's modular architecture principle
- Reduces code duplication and maintenance overhead

**Pattern**: Each Scaleway service wrapped in a Pulumi component with:
- Input validation using Pydantic models
- Output interfaces for dependency injection
- Standardized naming and tagging conventions
- Built-in monitoring and logging integration

### Environment Management

**Decision**: Stack-based configuration with environment-specific overlays

**Rationale**:
- Clear separation between infrastructure code and configuration
- Enables environment-specific scaling and security settings
- Supports zero-downtime deployments through blue-green patterns
- Aligns with Pulumi's recommended practices

**Pattern**: 
- Base infrastructure in components/
- Environment-specific stacks in stacks/
- Configuration models in config/ for type safety
- Shared utilities in lib/ for common patterns

## Security Implementation

### IAM and Secret Management

**Decision**: Scaleway IAM with Secret Manager integration

**Rationale**:
- Principle of least privilege through scoped IAM policies
- Centralized secret management with automatic rotation
- Audit trail for all access and changes
- Integration with existing Scaleway authentication

**Pattern**:
- Service-specific IAM roles with minimal permissions
- Secrets stored in Secret Manager with access controls
- Infrastructure components request secrets at deployment time
- No hardcoded credentials in infrastructure code

### Network Isolation

**Decision**: Scaleway Private Networks for service isolation

**Rationale**:
- Inter-service communication without public exposure
- Enhanced security through network segmentation
- Reduced attack surface and data transfer costs
- Compliance with security best practices

**Pattern**:
- Private network for each environment
- Service-specific subnets with controlled access
- Database access restricted to application containers only
- Monitoring endpoints accessible for operations team

## Testing Strategy

### Unit Testing

**Decision**: pytest with Pulumi's testing framework

**Rationale**:
- Leverages existing EvalAP testing infrastructure
- Pulumi provides isolated testing environment
- Fast feedback during development
- Integration with CI/CD pipeline

**Pattern**:
- Test each component in isolation with mocked dependencies
- Validate resource configurations and properties
- Test error handling and edge cases
- Coverage requirements aligned with EvalAP constitution

### Integration Testing

**Decision**: Full-stack testing with temporary environments

**Rationale**:
- Validates component interactions and dependencies
- Tests real Scaleway API interactions
- Verifies deployment and rollback procedures
- Confidence in production deployments

**Pattern**:
- Deploy complete infrastructure to temporary environment
- Run application deployment and connectivity tests
- Verify monitoring and alerting configurations
- Clean up test environment after validation

## Monitoring and Observability

### Cockpit Integration

**Decision**: Scaleway Cockpit for centralized monitoring

**Rationale**:
- Native integration with Scaleway services
- Comprehensive metrics, logs, and alerting
- Cost-effective for small team usage
- Simplified operations through single pane of glass

**Pattern**:
- Automatic metric collection from all infrastructure components
- Structured logging with correlation IDs
- Alert configurations for critical infrastructure events
- Dashboard templates for common operational views

## Cost Optimization

### Managed Services Selection

**Decision**: Prioritize managed services over self-hosted alternatives

**Rationale**:
- Reduced operational overhead and maintenance burden
- Built-in high availability and backup capabilities
- Predictable pricing with pay-as-you-go models
- Focus on application value rather than infrastructure management

**Pattern**:
- Serverless Containers for application hosting (no server management)
- Managed PostgreSQL with automated backups and failover
- Object Storage with lifecycle policies for cost optimization
- Cockpit for monitoring (no separate monitoring infrastructure)

## Edge Case Handling

### API Rate Limits

**Strategy**: Exponential backoff with jitter for retry logic

**Implementation**:
- Pulumi provider configuration with retry settings
- Custom retry wrapper for critical operations
- Monitoring of rate limit metrics and alerts
- Graceful degradation during peak usage

### Network Connectivity Issues

**Strategy**: Timeout configurations with circuit breaker pattern

**Implementation**:
- Configurable timeouts for all Scaleway API calls
- Circuit breaker to prevent cascade failures
- Local state caching for offline operations
- Manual intervention procedures for extended outages

### Credential Rotation

**Strategy**: Automated rotation with zero-downtime deployment

**Implementation**:
- Secret Manager integration for automatic rotation
- Blue-green deployment pattern for credential updates
- Validation of new credentials before cutover
- Rollback capability for failed rotations

## Conclusion

All technology decisions align with EvalAP's constitution and requirements:
- Sovereign Scaleway-only infrastructure
- Cost optimization through managed services
- Security by design with IAM and network isolation
- Comprehensive testing and monitoring
- Modular, reusable infrastructure components

The research phase confirms the feasibility of the proposed architecture and provides clear implementation patterns for the development phase.
