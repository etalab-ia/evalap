"""Test fixtures and mocks for Scaleway infrastructure testing."""

from typing import Any, Optional
from unittest.mock import Mock


class MockScalewayProvider:
    """Mock Scaleway provider for testing."""

    def __init__(self, region: str = "fr-par", project_id: str = "test-project"):
        """Initialize mock provider."""
        self.region = region
        self.project_id = project_id


class MockPulumiOutput:
    """Mock Pulumi output for testing."""

    def __init__(self, value: Any):
        """Initialize mock output with a value."""
        self.value = value

    def apply(self, func):
        """Apply a function to the output."""
        return MockPulumiOutput(func(self.value))

    def get_future(self):
        """Get future for the output."""
        future = Mock()
        future.result.return_value = self.value
        return future


class MockContainerNamespace:
    """Mock Scaleway container namespace."""

    def __init__(self, name: str = "test-namespace", id: str = "ns-123"):
        """Initialize mock container namespace."""
        self.name = name
        self.id = id
        self.endpoint = f"https://{name}.scw.cloud"


class MockContainer:
    """Mock Scaleway container."""

    def __init__(
        self,
        name: str = "test-container",
        id: str = "ctr-123",
        status: str = "ready",
    ):
        """Initialize mock container."""
        self.name = name
        self.id = id
        self.status = status
        self.endpoint = f"https://{name}.scw.cloud"


class MockDatabase:
    """Mock Scaleway managed database."""

    def __init__(
        self,
        name: str = "test-db",
        id: str = "db-123",
        status: str = "ready",
        host: str = "test-db.scw.cloud",
        port: int = 5432,
    ):
        """Initialize mock database."""
        self.name = name
        self.id = id
        self.status = status
        self.host = host
        self.port = port
        self.connection_string = f"postgresql://admin:password@{host}:{port}/{name}"


class MockObjectStorageBucket:
    """Mock Scaleway object storage bucket."""

    def __init__(
        self,
        name: str = "test-bucket",
        id: str = "bucket-123",
        region: str = "fr-par",
    ):
        """Initialize mock object storage bucket."""
        self.name = name
        self.id = id
        self.region = region
        self.endpoint = f"https://{name}.s3.{region}.scw.cloud"


class MockPrivateNetwork:
    """Mock Scaleway private network."""

    def __init__(
        self,
        name: str = "test-network",
        id: str = "pn-123",
        cidr: str = "10.0.0.0/16",
    ):
        """Initialize mock private network."""
        self.name = name
        self.id = id
        self.cidr = cidr


class MockSecretManager:
    """Mock Scaleway secret manager."""

    def __init__(self):
        """Initialize mock secret manager."""
        self.secrets = {}

    def create_secret(self, name: str, value: str) -> str:
        """Create a secret."""
        secret_id = f"secret-{len(self.secrets)}"
        self.secrets[name] = {"id": secret_id, "value": value}
        return secret_id

    def get_secret(self, name: str) -> Optional[str]:
        """Get a secret value."""
        if name in self.secrets:
            return self.secrets[name]["value"]
        return None

    def update_secret(self, name: str, value: str) -> bool:
        """Update a secret."""
        if name in self.secrets:
            self.secrets[name]["value"] = value
            return True
        return False

    def delete_secret(self, name: str) -> bool:
        """Delete a secret."""
        if name in self.secrets:
            del self.secrets[name]
            return True
        return False


def create_mock_stack_config() -> dict:
    """Create a mock stack configuration."""
    return {
        "stack_name": "test-stack",
        "environment": "dev",
        "region": "fr-par",
        "project_id": "test-project-123",
        "container": {
            "cpu": 1000,
            "memory": 1024,
            "max_concurrency": 100,
            "timeout": 300,
        },
        "database": {
            "engine": "PostgreSQL-15",
            "volume_size": 20,
            "backup_retention_days": 7,
            "enable_backups": True,
        },
        "storage": {
            "versioning_enabled": True,
            "acl": "private",
            "encryption_enabled": True,
        },
        "network": {
            "enable_private_network": False,
            "cidr_block": "10.0.0.0/16",
        },
        "monitoring": {
            "enable_cockpit": True,
            "metrics_retention_days": 30,
            "log_retention_days": 30,
        },
    }


def create_mock_provider_config() -> dict:
    """Create a mock provider configuration."""
    return {
        "region": "fr-par",
        "project_id": "test-project-123",
        "access_key": "test-access-key",
        "secret_key": "test-secret-key",
    }
