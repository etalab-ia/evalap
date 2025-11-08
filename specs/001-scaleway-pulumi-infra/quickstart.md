# Quickstart Guide: Scaleway Infrastructure with Pulumi

**Feature**: 001-scaleway-pulumi-infra | **Date**: 2025-11-08
**Target Audience**: Infrastructure developers, DevOps engineers

## Overview

This guide walks you through setting up and deploying infrastructure on Scaleway using Pulumi with Python SDK. You'll learn how to provision serverless containers, managed databases, object storage, and monitoring with complete infrastructure as code.

## Prerequisites

### Scaleway Account Setup

1. **Create Scaleway Account**
   - Sign up at https://console.scaleway.com/
   - Verify your email and phone number
   - Add payment method (required for some services)

2. **Generate API Credentials**
   ```bash
   # Install Scaleway CLI
   curl -s https://packagecloud.io/install/repositories/scaleway/script.deb.sh | sudo bash
   sudo apt-get install scw
   
   # Configure CLI
   scw init
   ```
   
   Or create credentials via web console:
   - Go to IAM → Applications → Create Application
   - Generate API keys (Access Key & Secret Key)

3. **Create Project**
   ```bash
   # Create project via CLI
   scw project create name="evalap-infra"
   
   # Note the project ID for later use
   ```

### Development Environment

1. **Python 3.12+**
   ```bash
   # Verify Python version
   python --version  # Should be 3.12 or higher
   ```

2. **Install Dependencies**
   ```bash
   # Add infrastructure dependencies to root pyproject.toml
   # Note: EvalAP uses centralized dependency management via uv
   
   # Install all dependencies including infra optional group
   uv sync --all-extras
   ```

3. **Install Pulumi CLI**
   ```bash
   # Install Pulumi CLI
   curl -fsSL https://get.pulumi.com | sh
   
   # Or via package manager
   # macOS: brew install pulumi
   # Ubuntu/Debian: See https://www.pulumi.com/docs/get-started/install/
   ```

## Environment Configuration

### 1. Set Up Environment Variables

Create `.env` file in repository root (copy from `.env.example`):

```bash
# Scaleway Configuration
SCW_ACCESS_KEY=SCWPxxxxxxxxxxxxxxxx
SCW_SECRET_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
SCW_PROJECT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
SCW_DEFAULT_REGION=fr-par-2
SCW_DEFAULT_ZONE=fr-par-2a

# Pulumi Configuration
PULUMI_CONFIG_PASSPHRASE=your-secure-passphrase
```

### 2. Configure Pulumi

```bash
# Login to Pulumi (using local backend for development)
pulumi login --local

# Set up encryption passphrase
export PULUMI_CONFIG_PASSPHRASE="your-secure-passphrase"
```

## Project Structure

Create the infrastructure directory structure:

```bash
mkdir -p infra/{components,stacks,config,lib,tests/{unit,integration,fixtures},docs}
```

## Basic Infrastructure Setup

### 1. Initialize Pulumi Project

```bash
cd infra

# Create new Pulumi project
pulumi new python --name "evalap-infra" --description "EvalAP Infrastructure on Scaleway"

# This creates:
# - Pulumi.yaml (project configuration)
# - __main__.py (entry point)
# - requirements.txt (Python dependencies)
# - .gitignore
```

### 2. Configure Pulumi Project

Edit `Pulumi.yaml`:

```yaml
name: evalap-infra
runtime: python
description: EvalAP Infrastructure on Scaleway
main: __main__.py

config:
  scaleway:region:
    type: string
    default: fr-par-2
  scaleway:project-id:
    type: string
  scaleway:access-key:
    type: string
    secret: true
  scaleway:secret-key:
    type: string
    secret: true
```

### 3. Set Up Provider Configuration

Create `infra/project.py`:

```python
"""Pulumi project setup and provider configuration."""

import os
import pulumi
import pulumi_scaleway as scaleway

def configure_provider():
    """Configure Scaleway provider with credentials."""
    
    # Get configuration values
    config = pulumi.Config()
    
    # Configure Scaleway provider
    provider = scaleway.Provider("scaleway-provider",
        region=config.get("scaleway:region") or os.getenv("SCW_DEFAULT_REGION", "fr-par-2"),
        project_id=config.get("scaleway:project-id") or os.getenv("SCW_PROJECT_ID"),
        access_key=config.get_secret("scaleway:access-key") or os.getenv("SCW_ACCESS_KEY"),
        secret_key=config.get_secret("scaleway:secret-key") or os.getenv("SCW_SECRET_KEY")
    )
    
    return provider

# Export provider for use in components
scaleway_provider = configure_provider()
```

### 4. Create Basic Stack

Create `infra/stacks/dev.py`:

```python
"""Development environment stack."""

import pulumi
from project import scaleway_provider
from components.serverless_container import ServerlessContainer
from components.database import DatabaseInstance
from components.object_storage import ObjectStorageBucket

class DevStack:
    """Development infrastructure stack."""
    
    def __init__(self):
        # Basic serverless container
        self.api_container = ServerlessContainer(
            "api-container",
            name="evalap-api-dev",
            image="ghcr.io/etalab-ia/evalap:latest",
            cpu_limit=1000,
            memory_limit=2048,
            min_scale=1,
            max_scale=2,
            environment_variables={
                "ENVIRONMENT": "development",
                "DEBUG": "true"
            },
            opts=pulumi.ResourceOptions(provider=scaleway_provider)
        )
        
        # Development database
        self.database = DatabaseInstance(
            "dev-database",
            name="evalap-db-dev",
            engine_version="15",
            node_type="db-dev-s",
            storage_size_gb=20,
            backup_retention_days=7,
            high_availability=False,
            opts=pulumi.ResourceOptions(provider=scaleway_provider)
        )
        
        # Storage for static assets
        self.storage = ObjectStorageBucket(
            "dev-storage",
            name="evalap-storage-dev-unique-name",
            region="fr-par-2",
            storage_class="standard",
            versioning_enabled=True,
            opts=pulumi.ResourceOptions(provider=scaleway_provider)
        )
        
        # Export stack outputs
        pulumi.export("api_endpoint", self.api_container.endpoint)
        pulumi.export("database_host", self.database.host)
        pulumi.export("storage_bucket", self.storage.name)

# Create stack instance
stack = DevStack()
```

### 5. Create Reusable Components

Create `infra/components/serverless_container.py`:

```python
"""Serverless container component."""

import pulumi
import pulumi_scaleway as scaleway

class ServerlessContainer(pulumi.ComponentResource):
    """Scaleway Serverless Container component."""
    
    def __init__(self, name: str, 
                 container_name: str,
                 image: str,
                 cpu_limit: int,
                 memory_limit: int,
                 min_scale: int = 1,
                 max_scale: int = 1,
                 environment_variables: dict = None,
                 opts: pulumi.ResourceOptions = None):
        
        super().__init__("evalap:components:ServerlessContainer", name, {}, opts)
        
        # Container namespace
        self.namespace = scaleway.ContainerNamespace(f"{name}-namespace",
            name=container_name,
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Container definition
        self.container = scaleway.Container(f"{name}-container",
            name=container_name,
            namespace_id=self.namespace.id,
            image=image,
            cpu_limit=cpu_limit,
            memory_limit=memory_limit,
            min_scale=min_scale,
            max_scale=max_scale,
            environment_variables=environment_variables or {},
            health_check={
                "protocol": "http",
                "path": "/health",
                "port": 8000,
                "interval_seconds": 30,
                "timeout_seconds": 5,
                "healthy_threshold": 2,
                "unhealthy_threshold": 3
            },
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Public endpoint
        self.endpoint = self.container.domain_name
        
        # Register outputs
        self.register_outputs({
            "endpoint": self.endpoint,
            "container_id": self.container.id,
            "namespace_id": self.namespace.id
        })
```

Create similar components for database and storage (see full implementation in project structure).

## Deployment Workflow

### 1. Preview Changes

```bash
cd infra

# Preview what will be created
pulumi preview

# Preview specific stack
pulumi preview --stack dev
```

### 2. Deploy Infrastructure

```bash
# Deploy to development
pulumi up --stack dev

# Confirm deployment when prompted
# Or auto-approve for automation
pulumi up --stack dev --yes
```

### 3. Verify Deployment

```bash
# Check stack status
pulumi stack output --stack dev

# Test container endpoint
curl $(pulumi stack output api_endpoint --stack dev)/health

# Connect to database (via psql or application)
```

### 4. Update Infrastructure

Modify your stack configuration and run:

```bash
# Preview changes
pulumi preview --stack dev

# Apply changes
pulumi up --stack dev --yes
```

### 5. Clean Up

```bash
# Destroy all resources in stack
pulumi destroy --stack dev --yes

# Remove stack
pulumi stack rm --stack dev --yes
```

## Environment Management

### 1. Create Staging Stack

```bash
# Create staging stack
pulumi stack init staging

# Configure staging-specific settings
pulumi config set scaleway:region fr-par-2 --stack staging
pulumi config set scaleway:project-id YOUR_PROJECT_ID --stack staging

# Deploy with staging configuration
pulumi up --stack staging
```

### 2. Environment-Specific Configurations

Create `infra/stacks/staging.py` with production-like settings:

```python
"""Staging environment stack."""

from components.serverless_container import ServerlessContainer
from components.database import DatabaseInstance

class StagingStack:
    def __init__(self):
        # Higher resource limits for staging
        self.api_container = ServerlessContainer(
            "api-container",
            name="evalap-api-staging",
            image="ghcr.io/etalab-ia/evalap:staging",
            cpu_limit=2000,
            memory_limit=4096,
            min_scale=1,
            max_scale=3,
            environment_variables={
                "ENVIRONMENT": "staging",
                "DEBUG": "false"
            }
        )
        
        # Database with HA for staging
        self.database = DatabaseInstance(
            "staging-database",
            name="evalap-db-staging",
            node_type="db-dev-m",
            storage_size_gb=50,
            high_availability=True,
            backup_retention_days=14
        )
```

## Testing Infrastructure

### 1. Unit Tests

Create `infra/tests/unit/test_serverless_container.py`:

```python
"""Unit tests for serverless container component."""

import pytest
from unittest.mock import Mock, patch
from components.serverless_container import ServerlessContainer

def test_serverless_container_creation():
    """Test serverless container component creation."""
    
    # Mock Pulumi resources
    with patch('pulumi_scaleway.ContainerNamespace') as mock_namespace, \
         patch('pulumi_scaleway.Container') as mock_container:
        
        # Create component
        container = ServerlessContainer(
            "test-container",
            container_name="test-api",
            image="nginx:latest",
            cpu_limit=1000,
            memory_limit=2048
        )
        
        # Verify resource creation
        mock_namespace.assert_called_once()
        mock_container.assert_called_once()
        
        # Verify configuration
        call_args = mock_container.call_args
        assert call_args[1]['cpu_limit'] == 1000
        assert call_args[1]['memory_limit'] == 2048
        assert call_args[1]['min_scale'] == 1
        assert call_args[1]['max_scale'] == 1

def test_serverless_container_validation():
    """Test configuration validation."""
    
    # Test invalid CPU limit
    with pytest.raises(ValueError):
        ServerlessContainer(
            "test-container",
            container_name="test-api",
            image="nginx:latest",
            cpu_limit=5000,  # Over limit
            memory_limit=2048
        )
```

### 2. Integration Tests

Create `infra/tests/integration/test_full_stack.py`:

```python
"""Integration tests for full infrastructure stack."""

import pytest
import requests
from stacks.dev import DevStack

@pytest.mark.integration
def test_full_stack_deployment():
    """Test complete infrastructure deployment."""
    
    # Deploy stack
    stack = DevStack()
    
    # Get outputs
    pulumi.up(stack_name="test-integration")
    
    api_endpoint = pulumi.get_stack().outputs["api_endpoint"]
    database_host = pulumi.get_stack().outputs["database_host"]
    
    # Test API endpoint
    response = requests.get(f"https://{api_endpoint}/health", timeout=30)
    assert response.status_code == 200
    
    # Test database connectivity
    # (Implementation depends on your database testing strategy)
    
    # Clean up
    pulumi.destroy(stack_name="test-integration")
```

### 3. Run Tests

```bash
# Run unit tests
pytest infra/tests/unit/ -v

# Run integration tests (requires real credentials)
pytest infra/tests/integration/ -v --integration

# Run all tests with coverage
pytest infra/tests/ --cov=infra --cov-report=html
```

## Monitoring and Observability

### 1. Enable Cockpit Monitoring

Add monitoring to your stack:

```python
from components.monitoring import MonitoringConfig

# In your stack definition
self.monitoring = MonitoringConfig(
    "monitoring",
    enabled=True,
    alert_channels=[
        {
            "name": "email-alerts",
            "type": "email",
            "target": "devops@etalab.gouv.fr"
        }
    ],
    metric_rules=[
        {
            "name": "high-cpu-usage",
            "metricName": "container_cpu_usage",
            "threshold": 80.0,
            "comparison": "gt",
            "severity": "warning"
        }
    ]
)
```

### 2. View Metrics

```bash
# Access Cockpit dashboard
echo "https://console.scaleway.com/cockpit/monitoring"

# View logs via CLI
scw container logs <container-id>
```

## Security Best Practices

### 1. Secret Management

```python
from components.secret_manager import Secret

# Store database credentials
self.db_secret = Secret(
    "db-credentials",
    name="evalap-db-credentials",
    secret_type="basic_auth",
    secret_data={
        "username": "evalap_user",
        "password": "secure_password_here"
    },
    rotation_enabled=True,
    rotation_period_days=90
)

# Reference secret in container
self.api_container = ServerlessContainer(
    "api-container",
    # ... other config
    environment_variables={
        "DB_HOST": self.database.host,
        "DB_USER": self.db_secret.username,
        "DB_PASSWORD": self.db_secret.password
    }
)
```

### 2. Network Isolation

```python
from components.private_network import PrivateNetwork

# Create private network
self.network = PrivateNetwork(
    "private-network",
    name="evalap-network",
    cidr="10.0.0.0/16",
    subnets=[
        {"name": "app-subnet", "cidr": "10.0.1.0/24"},
        {"name": "db-subnet", "cidr": "10.0.2.0/24"}
    ]
)

# Attach resources to private network
self.api_container = ServerlessContainer(
    "api-container",
    # ... other config
    network_config={
        "private_network_id": self.network.id,
        "subnet_ids": [self.network.app_subnet_id]
    }
)
```

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   ```bash
   # Verify credentials
   scw info
   
   # Check environment variables
   env | grep SCW_
   ```

2. **Resource Limits**
   ```bash
   # Check current quotas
   scw account quota list
   
   # Request quota increase if needed
   ```

3. **Deployment Failures**
   ```bash
   # Get detailed error information
   pulumi up --stack dev --debug
   
   # Check resource status
   scw container list
   scw rdb instance list
   ```

4. **State Lock Issues**
   ```bash
   # Force unlock state (use with caution)
   pulumi state unlock --stack dev
   ```

### Debug Commands

```bash
# Export current state
pulumi stack export --stack dev > state.json

# Inspect specific resources
pulumi state show <resource-urn> --stack dev

# Check configuration
pulumi config --stack dev
```

## Next Steps

1. **Production Setup**: Configure production stack with high availability and monitoring
2. **CI/CD Integration**: Set up GitHub Actions for automated deployments
3. **Cost Optimization**: Implement lifecycle policies and right-sizing
4. **Security Hardening**: Add network security groups and audit logging
5. **Backup Strategy**: Configure automated backups and disaster recovery

## Additional Resources

- [Pulumi Scaleway Provider Documentation](https://www.pulumi.com/registry/packages/scaleway/)
- [Scaleway Documentation](https://www.scaleway.com/en/docs/)
- [EvalAP Development Guide](../../docs/developer-guide/)
- [Project Constitution](../../../.specify/memory/constitution.md)

## Support

For issues with this infrastructure setup:
1. Check Scaleway service status: https://status.scaleway.com/
2. Review Pulumi documentation: https://www.pulumi.com/docs/
3. Open an issue in the EvalAP repository: https://github.com/etalab-ia/evalap/issues
