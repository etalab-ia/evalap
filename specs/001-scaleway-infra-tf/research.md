# Research: Scaleway Infrastructure Setup with Pure Terraform

**Date**: 2025-11-07  
**Purpose**: Research and decision documentation for Phase 0 of the planning process

## Technology Decisions

### Terraform vs Pure Terraform Approach

**Decision**: Use Pure Terraform (after extensive testing revealed Terragrunt is completely unusable)

#### Testing Results Summary

**Terragrunt v0.93.3 Testing**:
- ❌ **100% Failure Rate**: Every command crashes with segmentation faults
- ❌ **Critical Error**: `panic: runtime error: invalid memory address or nil pointer dereference`
- ❌ **Production Risk**: Completely unreliable for infrastructure deployment

**OpenTofu Consideration**:
- ✅ Open source alternative to Terraform
- ❌ **No Clear Benefit**: Terraform is already working perfectly
- ❌ **Added Complexity**: No compelling reason to switch from working Terraform

**Pure Terraform Results**:
- ✅ **100% Success Rate**: All commands work perfectly
- ✅ **Proven Reliability**: Battle-tested and stable
- ✅ **Simpler Debugging**: Direct error messages, no complex include chains
- ✅ **Better Security**: Easier credential handling
- ✅ **Faster Execution**: No include resolution overhead

#### Recommendation

**Use Pure Terraform** - The theoretical benefits of complex include systems (DRY configuration, hierarchical includes) are completely outweighed by their practical unreliability. Pure Terraform provides a robust, maintainable solution that works perfectly.

### Pure Terraform Configuration Management

**Decision**: Use Pure Terraform for configuration and environment management

**Rationale**:
- **Proven Reliability**: 100% success rate in testing vs 0% for Terragrunt
- **Simplicity**: Direct commands without complex include hierarchies
- **Better Debugging**: Clear error messages without include chain complexity
- **Security**: Easier to secure credential handling
- **Performance**: Faster execution without include resolution overhead
- **Maintainability**: Fewer moving parts, easier to understand and troubleshoot

**Implementation Approach**:
- Separate environment directories (staging/, production/)
- Shared modules in modules/ directory
- Environment-specific terraform.tfvars files
- Deployment scripts for automation (deploy_staging_terraform.sh)
- Direct terraform commands for all operations

**Alternatives Considered**:
- Pure Terraform with workspaces - Rejected due to complex state management
- Terraform Cloud/Enterprise - Rejected due to third-party service constraint (FR-013)

### Scaleway Provider Strategy

**Decision**: Use Scaleway Terraform Provider v2.0+ with official modules

**Rationale**:
- Native Scaleway integration with full feature support
- Provider maintained by Scaleway with regular updates
- Supports all required services (Containers, PostgreSQL, Cockpit, Secret Manager)
- French/European sovereign cloud provider (M3 principle)
- Competitive pricing and performance

**Alternatives Considered**:
- Custom provider wrappers - Rejected due to maintenance overhead
- Multi-cloud approach - Rejected due to complexity and FR-013 constraint

### Container Registry Integration

**Decision**: Build and push to Scaleway Container Registry during deployment

**Rationale**:
- Integrated with Scaleway ecosystem (no external dependencies)
- Simplified access control through IAM policies
- Same region as compute resources (performance benefits)
- Cost-effective for government projects
- Supports private repositories for security

**Alternatives Considered**:
- Docker Hub - Rejected due to external service dependency
- GitHub Packages - Rejected due to third-party service constraint

## Architecture Patterns

### Zero-Downtime Deployment Strategy

**Decision**: Rolling updates with instance-by-instance replacement

**Rationale**:
- Leverages Scaleway Serverless Containers built-in load balancing
- Simpler than blue-green deployments for container-based services
- Gradual rollout allows monitoring of each instance
- Maintains service availability during updates
- Aligns with 99.5% uptime requirement

**Implementation Approach**:
- Deploy new container version alongside existing
- Gradually shift traffic to new instances
- Monitor health and rollback if issues detected
- Complete cutover when all instances healthy

### Environment Isolation Strategy

**Decision**: Separate infrastructure deployments with container image promotion

**Rationale**:
- Complete isolation prevents cross-environment contamination
- Independent scaling and configuration per environment
- Simplified security boundaries
- Clear audit trail for changes
- Aligns with FR-006 requirement

**Implementation Approach**:
- Separate Terraform state per environment
- Shared container registry with image promotion
- Environment-specific configurations via Terraform
- Independent IAM policies per environment

### Database Migration Integration

**Decision**: Alembic migrations triggered automatically during deployment

**Rationale**:
- Leverages existing EvalAP database migration system
- Ensures schema changes are version-controlled
- Automatic integration prevents human error
- Supports rollback scenarios
- Aligns with existing development workflow

**Implementation Approach**:
- GitHub Actions workflow runs `alembic upgrade head` before service deployment
- Migration status tracked in deployment logs
- Rollback includes database schema rollback capability

## Security Considerations

### Secret Management Strategy

**Decision**: Scaleway IAM Secret Manager with automatic injection

**Rationale**:
- Centralized secret management with audit trails
- Integration with Scaleway IAM for access control
- Automatic rotation capabilities
- No hardcoded secrets in configuration (FR-016)
- Supports compliance requirements

**Implementation Approach**:
- Secrets stored in IAM Secret Manager
- Container environment variables populated at runtime
- Access controlled through least-privilege IAM policies
- Regular secret rotation schedules

### Network Security

**Decision**: Scaleway VPC with private networking where applicable

**Rationale**:
- Isolates infrastructure components
- Reduces attack surface
- Enables secure communication between services
- Supports compliance requirements

**Implementation Approach**:
- Private endpoints for database access
- Container networking within VPC
- Internet access through managed gateways

## Performance Optimization

### Scaling Strategy

**Decision**: Automatic scaling with configured min/max limits

**Rationale**:
- Cost-effective resource utilization
- Handles traffic spikes automatically
- Maintains performance under load
- Supports 99.5% uptime requirement

**Implementation Approach**:
- Production: Minimum 2 instances per service (redundancy)
- Configured maximum limits based on expected load
- Health checks trigger automatic replacement
- Metrics-driven scaling decisions

### Monitoring Integration

**Decision**: Scaleway Cockpit with custom alerting

**Rationale**:
- Native integration with Scaleway services
- Comprehensive metrics and logging
- Automated alerting for SLA compliance
- Supports 30-second alerting requirement (SC-009)

**Implementation Approach**:
- Default metrics for all Scaleway services
- Custom application metrics via endpoints
- Alert thresholds aligned with SLA requirements
- Integration with GitHub Actions for deployment notifications

## Cost Management

### Resource Optimization

**Decision**: Right-sized resources with automatic scaling

**Rationale**:
- Cost-effective for government budgets
- Pay-for-what-you-use model
- Automatic scaling prevents over-provisioning
- Supports sustainability goals

**Implementation Approach**:
- Appropriate instance sizes per service
- Scale-to-zero for non-critical services
- Regular cost review and optimization
- Backup retention policies aligned with compliance (30/90/365 days)

## Compliance Considerations

### Data Protection

**Decision**: Data residency within EU/Scaleway infrastructure

**Rationale**:
- GDPR compliance requirements
- French government data sovereignty
- Performance benefits of regional deployment
- Supports compliance audit requirements

**Implementation Approach**:
- All infrastructure in fr-par region
- Data encryption at rest and in transit
- Audit trails for all data access
- Regular compliance assessments

## Risk Mitigation

### High Availability

**Decision**: Multi-AZ deployment where supported

**Rationale**:
- Meets 99.5% uptime SLA
- Protects against infrastructure failures
- Supports automatic failover requirements
- Reduces single points of failure

**Implementation Approach**:
- Database with automatic failover
- Container distribution across availability zones
- Health monitoring and automatic recovery
- Disaster recovery procedures documented

### Deployment Risk

**Decision**: Comprehensive testing and rollback procedures

**Rationale**:
- Minimizes deployment-related outages
- Supports 2-minute rollback requirement (SC-003)
- Enables rapid recovery from issues
- Maintains service availability

**Implementation Approach**:
- Staging environment for validation
- Automated testing before production deployment
- One-click rollback procedures
- Deployment monitoring and alerting

## Conclusion

All research decisions align with:
- French government AI principles (open source, sovereignty)
- EvalAP constitution (modular architecture, observability)
- Feature requirements (99.5% uptime, zero-downtime deployments)
- Security and compliance requirements (GDPR, data protection)

The chosen technology stack provides:
- Simplified management compared to CDKTF
- Complete Scaleway ecosystem integration
- Robust security and compliance capabilities
- Cost-effective scaling and operations

**Ready for Phase 1**: Design and contract generation.
