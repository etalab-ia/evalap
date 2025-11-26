"""Unit tests for configuration models."""

import pytest
from pydantic import ValidationError

from infra.config.models import (
    ContainerConfig,
    DatabaseConfig,
    MonitoringConfig,
    NetworkConfig,
    StackConfiguration,
    StorageConfig,
)


class TestContainerConfig:
    """Tests for ContainerConfig model."""

    def test_valid_container_config(self):
        """Test creating a valid container configuration."""
        config = ContainerConfig(
            cpu=500,
            memory=512,
        )
        assert config.cpu == 500
        assert config.memory == 512
        assert config.max_concurrency == 80
        assert config.timeout == 300

    def test_container_cpu_too_low(self):
        """Test that CPU below minimum is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ContainerConfig(
                cpu=50,  # Below minimum of 100
                memory=512,
            )
        assert "cpu" in str(exc_info.value)

    def test_container_cpu_too_high(self):
        """Test that CPU above maximum is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ContainerConfig(
                cpu=5000,  # Above maximum of 4000
                memory=512,
            )
        assert "cpu" in str(exc_info.value)

    def test_container_memory_too_low(self):
        """Test that memory below minimum is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ContainerConfig(
                cpu=500,
                memory=64,  # Below minimum of 128
            )
        assert "memory" in str(exc_info.value)

    def test_container_memory_too_high(self):
        """Test that memory above maximum is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ContainerConfig(
                cpu=500,
                memory=9000,  # Above maximum of 8192
            )
        assert "memory" in str(exc_info.value)

    def test_container_memory_cpu_ratio_validation(self):
        """Test that memory must be appropriate for CPU allocation."""
        with pytest.raises(ValidationError) as exc_info:
            ContainerConfig(
                cpu=100,
                memory=5000,  # Too high for 100m CPU (max should be 800)
            )
        assert "memory" in str(exc_info.value).lower()

    def test_container_defaults(self):
        """Test that container has sensible defaults."""
        config = ContainerConfig()
        assert config.cpu == 1000
        assert config.memory == 1024
        assert config.max_concurrency == 80
        assert config.timeout == 300


class TestDatabaseConfig:
    """Tests for DatabaseConfig model."""

    def test_valid_database_config(self):
        """Test creating a valid database configuration."""
        config = DatabaseConfig(
            engine="PostgreSQL-15",
            volume_size=20,
            backup_retention_days=7,
        )
        assert config.engine == "PostgreSQL-15"
        assert config.volume_size == 20
        assert config.backup_retention_days == 7
        assert config.enable_backups is True
        assert config.enable_high_availability is False

    def test_database_volume_too_small(self):
        """Test that volume below minimum is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            DatabaseConfig(
                volume_size=2,  # Below minimum of 5
            )
        assert "volume_size" in str(exc_info.value)

    def test_database_volume_too_large(self):
        """Test that volume above maximum is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            DatabaseConfig(
                volume_size=600,  # Above maximum of 500
            )
        assert "volume_size" in str(exc_info.value)

    def test_database_backup_retention_too_low(self):
        """Test that backup retention below minimum is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            DatabaseConfig(
                backup_retention_days=0,  # Below minimum of 1
            )
        assert "backup_retention_days" in str(exc_info.value)

    def test_database_backup_retention_too_high(self):
        """Test that backup retention above maximum is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            DatabaseConfig(
                backup_retention_days=400,  # Above maximum of 365
            )
        assert "backup_retention_days" in str(exc_info.value)

    def test_database_defaults(self):
        """Test that database has sensible defaults."""
        config = DatabaseConfig()
        assert config.engine == "PostgreSQL-15"
        assert config.volume_size == 20
        assert config.backup_retention_days == 7
        assert config.user_name == "postgres"
        assert config.database_name == "evalap"


class TestStorageConfig:
    """Tests for StorageConfig model."""

    def test_valid_storage_config(self):
        """Test creating a valid storage configuration."""
        config = StorageConfig(
            versioning_enabled=True,
            lifecycle_expiration_days=90,
        )
        assert config.versioning_enabled is True
        assert config.lifecycle_expiration_days == 90
        assert config.acl == "private"
        assert config.encryption_enabled is True

    def test_storage_defaults(self):
        """Test that storage has sensible defaults."""
        config = StorageConfig()
        assert config.versioning_enabled is True
        assert config.lifecycle_expiration_days is None
        assert config.acl == "private"
        assert config.encryption_enabled is True


class TestNetworkConfig:
    """Tests for NetworkConfig model."""

    def test_valid_network_config(self):
        """Test creating a valid network configuration."""
        config = NetworkConfig(
            enable_private_network=True,
            cidr_block="10.0.0.0/16",
            enable_nat_gateway=True,
        )
        assert config.enable_private_network is True
        assert config.cidr_block == "10.0.0.0/16"
        assert config.enable_nat_gateway is True

    def test_network_defaults(self):
        """Test that network has sensible defaults."""
        config = NetworkConfig()
        assert config.enable_private_network is False
        assert config.cidr_block == "10.0.0.0/16"
        assert config.enable_nat_gateway is False


class TestMonitoringConfig:
    """Tests for MonitoringConfig model."""

    def test_valid_monitoring_config(self):
        """Test creating a valid monitoring configuration."""
        config = MonitoringConfig(
            enable_cockpit=True,
            metrics_retention_days=30,
        )
        assert config.enable_cockpit is True
        assert config.metrics_retention_days == 30
        assert config.log_retention_days == 30
        assert config.enable_alerts is True

    def test_monitoring_retention_days_default(self):
        """Test that retention days has a default value."""
        config = MonitoringConfig()
        assert config.metrics_retention_days == 30
        assert config.log_retention_days == 30

    def test_monitoring_retention_too_low(self):
        """Test that retention below minimum is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            MonitoringConfig(metrics_retention_days=0)
        assert "metrics_retention_days" in str(exc_info.value)

    def test_monitoring_retention_too_high(self):
        """Test that retention above maximum is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            MonitoringConfig(metrics_retention_days=400)
        assert "metrics_retention_days" in str(exc_info.value)


class TestStackConfiguration:
    """Tests for StackConfiguration model."""

    def test_valid_stack_configuration(self):
        """Test creating a valid stack configuration."""
        config = StackConfiguration(
            stack_name="dev-stack",
            environment="dev",
            region="fr-par",
            project_id="test-project-123",
        )

        assert config.stack_name == "dev-stack"
        assert config.environment == "dev"
        assert config.region == "fr-par"
        assert config.project_id == "test-project-123"
        assert isinstance(config.container, ContainerConfig)
        assert isinstance(config.database, DatabaseConfig)
        assert isinstance(config.storage, StorageConfig)
        assert isinstance(config.network, NetworkConfig)
        assert isinstance(config.monitoring, MonitoringConfig)

    def test_stack_configuration_stack_name_required(self):
        """Test that stack name is required."""
        with pytest.raises(ValidationError) as exc_info:
            StackConfiguration(
                environment="dev",
                region="fr-par",
                project_id="test-project-123",
            )
        assert "stack_name" in str(exc_info.value)

    def test_stack_configuration_environment_required(self):
        """Test that environment is required."""
        with pytest.raises(ValidationError) as exc_info:
            StackConfiguration(
                stack_name="dev-stack",
                region="fr-par",
                project_id="test-project-123",
            )
        assert "environment" in str(exc_info.value)

    def test_stack_configuration_project_id_required(self):
        """Test that project ID is required."""
        with pytest.raises(ValidationError) as exc_info:
            StackConfiguration(
                stack_name="dev-stack",
                environment="dev",
                region="fr-par",
            )
        assert "project_id" in str(exc_info.value)

    def test_stack_configuration_invalid_environment(self):
        """Test that invalid environment is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            StackConfiguration(
                stack_name="dev-stack",
                environment="invalid",  # Not in allowed set
                region="fr-par",
                project_id="test-project-123",
            )
        assert "environment" in str(exc_info.value)

    def test_stack_configuration_valid_environments(self):
        """Test that all valid environments are accepted."""
        for env in ["dev", "staging", "production"]:
            config = StackConfiguration(
                stack_name=f"{env}-stack",
                environment=env,
                region="fr-par",
                project_id="test-project-123",
            )
            assert config.environment == env

    def test_stack_configuration_with_custom_components(self):
        """Test creating stack with custom component configurations."""
        container = ContainerConfig(cpu=2000, memory=2048)
        database = DatabaseConfig(volume_size=100, backup_retention_days=30)
        storage = StorageConfig(versioning_enabled=False)
        network = NetworkConfig(enable_private_network=True)
        monitoring = MonitoringConfig(enable_cockpit=False)

        config = StackConfiguration(
            stack_name="custom-stack",
            environment="staging",
            region="nl-ams",
            project_id="test-project-456",
            container=container,
            database=database,
            storage=storage,
            network=network,
            monitoring=monitoring,
        )

        assert config.container.cpu == 2000
        assert config.database.volume_size == 100
        assert config.storage.versioning_enabled is False
        assert config.network.enable_private_network is True
        assert config.monitoring.enable_cockpit is False

    def test_stack_configuration_tags(self):
        """Test that tags can be set on stack configuration."""
        config = StackConfiguration(
            stack_name="tagged-stack",
            environment="dev",
            region="fr-par",
            project_id="test-project-789",
            tags={"team": "platform", "cost-center": "engineering"},
        )

        assert config.tags["team"] == "platform"
        assert config.tags["cost-center"] == "engineering"
