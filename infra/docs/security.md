# Security Configuration Guide

This document describes the security configuration for EvalAP infrastructure on Scaleway, covering IAM policies, secret management, and network isolation.

## Overview

EvalAP implements a defense-in-depth security model with three layers:

1. **IAM Policies**: Service-specific role definitions with least privilege access
2. **Secret Manager**: Secure credential storage with versioning and rotation support
3. **Private Networks**: Service isolation via VPC for secure inter-service communication

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Security Architecture                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │  IAM Policy  │    │   Secrets    │    │   Private    │          │
│  │  (Identity)  │    │  (Credentials)│    │   Network    │          │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘          │
│         │                   │                   │                   │
│         ▼                   ▼                   ▼                   │
│  ┌──────────────────────────────────────────────────────┐          │
│  │              Serverless Containers                    │          │
│  │  - API Service                                        │          │
│  │  - Runners Service                                    │          │
│  │  - Documentation Service                              │          │
│  └──────────────────────────────────────────────────────┘          │
│                            │                                        │
│                            ▼                                        │
│  ┌──────────────────────────────────────────────────────┐          │
│  │              Managed PostgreSQL                       │          │
│  │  (Private network access only)                        │          │
│  └──────────────────────────────────────────────────────┘          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## IAM Configuration

### Principle of Least Privilege

All IAM policies follow the principle of least privilege:

- **Project-scoped access**: Permissions are scoped to specific projects, never organization-wide
- **Service-specific roles**: Each service gets only the permissions it needs
- **Read-only by default**: Use read-only access unless write access is required

### Permission Sets Reference

Scaleway IAM uses predefined permission sets. The following are used in EvalAP:

| Service               | Permission Set                  | Description                    |
| --------------------- | ------------------------------- | ------------------------------ |
| Serverless Containers | `ContainersFullAccess`          | Deploy and manage containers   |
| Serverless Containers | `ContainersReadOnly`            | View container status only     |
| Database              | `RelationalDatabasesFullAccess` | Manage PostgreSQL instances    |
| Database              | `RelationalDatabasesReadOnly`   | View database status only      |
| Object Storage        | `ObjectStorageFullAccess`       | Read/write objects and buckets |
| Object Storage        | `ObjectStorageReadOnly`         | Read objects only              |
| Secret Manager        | `SecretManagerSecretAccess`     | Read secrets (not manage)      |
| Secret Manager        | `SecretManagerReadOnly`         | View secret metadata only      |
| Container Registry    | `ContainerRegistryFullAccess`   | Push and pull images           |
| Container Registry    | `ContainerRegistryReadOnly`     | Pull images only               |
| Cockpit               | `ObservabilityReadOnly`         | View metrics and logs          |

### Predefined Policies

#### EvalAP Service Policy

The standard service policy for EvalAP applications:

```python
from infra.components.iam_policy import create_evalap_service_policy

policy = create_evalap_service_policy(
    environment="production",
    project_id="your-project-id",
)
policy.create()
```

This creates a policy with:

| Service               | Access Level  | Rationale                    |
| --------------------- | ------------- | ---------------------------- |
| Serverless Containers | Full Access   | Deploy and manage containers |
| Database              | Full Access   | Manage PostgreSQL            |
| Object Storage        | Full Access   | Store artifacts              |
| Secret Manager        | Secret Access | Read secrets only            |
| Container Registry    | Read Only     | Pull images                  |
| Cockpit               | Read Only     | View metrics                 |

#### CI/CD Pipeline Policy

For GitHub Actions and deployment pipelines:

```python
from infra.components.iam_policy import create_ci_cd_policy

policy = create_ci_cd_policy(
    environment="production",
    project_id="your-project-id",
)
policy.create()
```

This creates a policy with:

| Service               | Access Level | Rationale               |
| --------------------- | ------------ | ----------------------- |
| Serverless Containers | Full Access  | Deploy containers       |
| Container Registry    | Full Access  | Push images             |
| Secret Manager        | Read Only    | Read deployment secrets |
| Cockpit               | Read Only    | View deployment metrics |

#### Read-Only Policy

For monitoring and auditing:

```python
from infra.components.iam_policy import create_readonly_policy

policy = create_readonly_policy(
    name="evalap-readonly",
    environment="production",
    project_id="your-project-id",
)
policy.create()
```

### Custom Policy Configuration

For custom policies, use `IAMPolicy` directly:

```python
from infra.components.iam_policy import IAMPolicy, IAMPolicyConfig, ServiceType

rules = [
    IAMPolicyConfig(
        service=ServiceType.OBJECT_STORAGE,
        access_level="read_only",
        project_ids=["your-project-id"],
    ),
    IAMPolicyConfig(
        service=ServiceType.COCKPIT,
        access_level="logs_only",
        project_ids=["your-project-id"],
    ),
]

policy = IAMPolicy(
    name="custom-policy",
    environment="production",
    description="Custom read-only policy for monitoring",
    rules=rules,
)
policy.create()
```

### IAM Validation

The infrastructure includes validation to enforce least privilege:

```python
from infra.utils.validation import validate_least_privilege

# This will raise ValueError if rules violate least privilege
validate_least_privilege(
    rules=policy_rules,
    required_services=["object_storage", "cockpit"],
)
```

Validation checks:

- No unnecessary services have permissions
- No organization-wide access (must be project-scoped)
- Valid service and access level combinations

## Secret Management

### Overview

Secrets are stored in Scaleway Secret Manager with:

- **Immutable versioning**: Each update creates a new version
- **Encryption at rest**: All secrets encrypted by Scaleway
- **Access control**: IAM policies control who can read secrets
- **Audit logging**: All access is logged

### Secret Types

| Type                   | Use Case                   |
| ---------------------- | -------------------------- |
| `opaque`               | Generic secrets (default)  |
| `database_credentials` | Database username/password |
| `basic_credentials`    | Username/password pairs    |
| `certificate`          | TLS certificates           |
| `ssh_key`              | SSH keys                   |
| `key_value`            | Key-value pairs            |

### Creating Secrets

```python
from infra.components.secret_manager import SecretManager
from infra.config.models import SecretConfig

secrets = SecretManager(
    name="evalap-secrets",
    environment="production",
    configs=[
        SecretConfig(
            name="db-password",
            description="PostgreSQL admin password",
            data="your-secure-password",
            path="/evalap/database",
            secret_type="database_credentials",
            protected=True,  # Prevent accidental deletion
        ),
        SecretConfig(
            name="api-key",
            description="External API key",
            data="your-api-key",
            path="/evalap/api",
            secret_type="opaque",
        ),
    ],
    project_id="your-project-id",
    region="fr-par",
)
secrets.create()
```

### Injecting Secrets into Containers

Secrets can be injected as environment variables:

```python
# Get secrets for container environment
env_vars = secrets.get_secrets_for_container({
    "db-password": "DATABASE_PASSWORD",
    "api-key": "API_KEY",
})

# Use in container configuration
container = ServerlessContainer(
    name="api",
    environment="production",
    config=ContainerConfig(
        secret_environment_variables=env_vars,
    ),
    # ...
)
```

### Secret Rotation

To rotate a secret, create a new version:

```python
# Create new version (old version remains immutable)
new_version_id = secrets.update_secret_version(
    secret_name="db-password",
    new_data="new-secure-password",
    description="Rotated on 2024-01-15",
)
```

**Important**: After rotation, redeploy containers to pick up the new secret version.

### Secret Naming Convention

Secrets follow this naming pattern:

```
{name}-{environment}
```

Example: `db-password-production`

Path organization:

```
/evalap/
├── database/
│   ├── db-password-production
│   └── db-password-staging
├── api/
│   ├── api-key-production
│   └── api-key-staging
└── external/
    └── llm-api-key-production
```

## Network Isolation

### Private Network Architecture

Private networks provide service isolation:

```
┌─────────────────────────────────────────────────────────────┐
│                    VPC (evalap-vpc-production)               │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          Private Network (10.0.0.0/16)                  │ │
│  │                                                          │ │
│  │  ┌──────────────┐    ┌──────────────┐                   │ │
│  │  │  Container   │◄──►│  PostgreSQL  │                   │ │
│  │  │  (API)       │    │  (Database)  │                   │ │
│  │  │  10.0.1.x    │    │  10.0.2.x    │                   │ │
│  │  └──────────────┘    └──────────────┘                   │ │
│  │                                                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │    Internet      │
                    │  (Public Access) │
                    └──────────────────┘
```

### Enabling Private Networks

```python
from infra.components.private_network import PrivateNetwork
from infra.config.models import NetworkConfig

network = PrivateNetwork(
    name="evalap-network",
    environment="production",
    config=NetworkConfig(
        enable_private_network=True,
        cidr_block="10.0.0.0/16",
    ),
    project_id="your-project-id",
    region="fr-par",
)
network.create()
```

### Connecting Services to Private Network

#### Database Connection

```python
from infra.components.database import DatabaseInstance

database = DatabaseInstance(
    name="evalap-db",
    environment="production",
    config=database_config,
    project_id="your-project-id",
    private_network_id=network.get_private_network_id(),
)
database.create()
```

#### Container Connection

```python
from infra.components.serverless_container import ServerlessContainer

container = ServerlessContainer(
    name="api",
    environment="production",
    config=container_config,
    project_id="your-project-id",
    private_network_config=network.get_container_private_network_config(),
)
container.create()
```

**Note**: Private network integration with Serverless Containers is a beta feature. The container namespace must have `activate_vpc_integration=true`.

### CIDR Block Guidelines

Use RFC 1918 private address ranges:

| Range   | CIDR             | Available IPs |
| ------- | ---------------- | ------------- |
| Class A | `10.0.0.0/8`     | 16,777,216    |
| Class B | `172.16.0.0/12`  | 1,048,576     |
| Class C | `192.168.0.0/16` | 65,536        |

Recommended for EvalAP:

- **Development**: `10.0.0.0/24` (256 IPs)
- **Staging**: `10.1.0.0/24` (256 IPs)
- **Production**: `10.2.0.0/16` (65,536 IPs)

### Network Validation

```python
from infra.utils.validation import validate_cidr_block, validate_private_network_cidr

# Validate CIDR format
validate_cidr_block("10.0.0.0/16")  # Returns True

# Validate it's a private range
validate_private_network_cidr("10.0.0.0/16")  # Returns True
validate_private_network_cidr("8.8.8.0/24")   # Raises ValueError
```

## Security Best Practices

### 1. Never Hardcode Secrets

❌ **Wrong**:

```python
database_password = "my-secret-password"
```

✅ **Correct**:

```python
import os
database_password = os.environ.get("DATABASE_PASSWORD")
# Or use Secret Manager
```

### 2. Use Environment-Specific Secrets

Each environment should have its own secrets:

```python
secrets = SecretManager(
    name="evalap-secrets",
    environment=environment,  # "dev", "staging", "production"
    configs=[...],
)
```

### 3. Protect Production Secrets

Enable protection for production secrets:

```python
SecretConfig(
    name="db-password",
    data="...",
    protected=True,  # Prevents accidental deletion
)
```

### 4. Scope IAM to Projects

Always use project-scoped permissions:

```python
IAMPolicyConfig(
    service=ServiceType.DATABASE,
    access_level="full_access",
    project_ids=["specific-project-id"],  # ✅ Project-scoped
    # organization_id="...",  # ❌ Avoid organization-wide
)
```

### 5. Use Private Networks for Databases

Never expose databases to the public internet:

```python
NetworkConfig(
    enable_private_network=True,  # ✅ Required for production
)
```

### 6. Rotate Secrets Regularly

Implement a rotation schedule:

| Secret Type          | Rotation Frequency |
| -------------------- | ------------------ |
| Database passwords   | 90 days            |
| API keys             | 180 days           |
| Service account keys | 365 days           |

### 7. Audit Access Logs

Monitor secret access via Scaleway Cockpit:

1. Go to Scaleway Console → Cockpit
2. Navigate to Logs
3. Filter by `secret_manager` service
4. Review access patterns

## Troubleshooting

### IAM Permission Denied

**Symptom**: `403 Forbidden` when accessing resources

**Solution**:

1. Verify the IAM application has the correct policy attached
2. Check that the policy rules include the required permission set
3. Ensure the policy is scoped to the correct project ID

```bash
# List IAM policies
scw iam policy list
```

### Secret Not Found

**Symptom**: `Secret not found` error

**Solution**:

1. Verify the secret exists in the correct region
2. Check the secret path matches the expected format
3. Ensure the IAM policy has `SecretManagerSecretAccess` permission

```bash
# List secrets
scw secret-manager secret list region=fr-par
```

### Private Network Connection Failed

**Symptom**: Container cannot reach database

**Solution**:

1. Verify both resources are in the same private network
2. Check the VPC has routing enabled
3. Ensure the container namespace has VPC integration activated

```bash
# List private networks
scw vpc private-network list region=fr-par
```

## Related Documentation

- [State Management](./state_management.md) - Pulumi state backend configuration
- [Scaleway IAM Reference](https://www.scaleway.com/en/docs/iam/reference-content/permission-sets/)
- [Scaleway Secret Manager](https://www.scaleway.com/en/docs/secret-manager/)
- [Scaleway VPC](https://www.scaleway.com/en/docs/vpc/)
