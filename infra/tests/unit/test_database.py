"""Unit tests for DatabaseInstance component."""

from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from infra.components.database import DatabaseInstance
from infra.components.secret_manager import SecretManager
from infra.config.models import DatabaseConfig, SecretConfig


class TestDatabaseInstance:
    """Tests for DatabaseInstance component."""

    @pytest.fixture
    def database_config(self):
        """Create a valid database configuration for testing."""
        return DatabaseConfig(
            engine="PostgreSQL-15",
            volume_size=50,
            backup_retention_days=14,
            enable_backups=True,
            enable_high_availability=False,
            user_name="testuser",
            database_name="testdb",
        )

    @pytest.fixture
    def database_instance(self, database_config):
        """Create a DatabaseInstance instance for testing."""
        return DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            region="fr-par",
            tags={"team": "platform"},
        )

    def test_database_instance_initialization(self, database_instance, database_config):
        """Test that DatabaseInstance initializes correctly."""
        assert database_instance.name == "test-database"
        assert database_instance.environment == "dev"
        assert database_instance.config == database_config
        assert database_instance.project_id == "test-project-123"
        assert database_instance.region == "fr-par"
        assert database_instance.tags == {"team": "platform"}
        assert database_instance.instance is None
        assert database_instance.database is None
        assert database_instance.user is None

    def test_database_instance_initialization_with_defaults(self):
        """Test DatabaseInstance initialization with minimal parameters."""
        config = DatabaseConfig()
        db = DatabaseInstance(
            name="minimal-database",
            environment="staging",
            config=config,
            project_id="test-project-456",
        )

        assert db.name == "minimal-database"
        assert db.environment == "staging"
        assert db.region == "fr-par"  # Default value
        assert db.tags == {}  # Default empty dict

    def test_database_instance_invalid_volume_size_validation(self):
        """Test that invalid volume size raises validation error."""
        with pytest.raises(ValidationError):
            DatabaseConfig(volume_size=2)  # Too small

    def test_database_instance_invalid_backup_retention_validation(self):
        """Test that invalid backup retention raises validation error."""
        with pytest.raises(ValidationError):
            DatabaseConfig(backup_retention_days=400)  # Too high

    def test_database_instance_invalid_database_name_validation(self):
        """Test that invalid database name raises validation error."""
        invalid_config = DatabaseConfig(database_name="invalid-db-name-with-special-chars!")

        with pytest.raises(ValueError):
            DatabaseInstance(
                name="invalid-database",
                environment="dev",
                config=invalid_config,
                project_id="test-project-123",
            )

    @patch("infra.components.database.scaleway.databases.Instance")
    @patch("infra.components.database.scaleway.databases.Database")
    @patch("infra.components.database.pulumi_helpers.log_resource_creation")
    def test_create_success(self, mock_log, mock_database_class, mock_instance_class, database_instance):
        """Test successful creation of database infrastructure."""
        # Mock the instance and database objects
        mock_instance = MagicMock()
        mock_database = MagicMock()
        mock_instance_class.return_value = mock_instance
        mock_database_class.return_value = mock_database

        # Mock the config secret
        with patch("infra.components.database.pulumi.Config") as mock_config_class:
            mock_config = MagicMock()
            mock_config.require_secret.return_value = "secret-password"
            mock_config_class.return_value = mock_config

            # Call create method
            database_instance.create()

        # Verify logging was called
        mock_log.assert_called_once_with(
            "DatabaseInstance",
            "test-database",
            environment="dev",
            engine="PostgreSQL-15",
            volume_size=50,
            backup_retention=14,
        )

        # Verify instance was created
        mock_instance_class.assert_called_once()
        instance_args = mock_instance_class.call_args[1]
        assert instance_args["name"] == "test-database-db-dev"
        assert instance_args["engine"] == "PostgreSQL-15"
        assert instance_args["node_type"] == "DB-DEV-S"
        assert instance_args["is_ha_cluster"] is False
        assert instance_args["project_id"] == "test-project-123"
        assert instance_args["region"] == "fr-par"

        # Verify database was created
        mock_database_class.assert_called_once()
        database_args = mock_database_class.call_args[1]
        assert database_args["name"] == "testdb"

    @patch("infra.components.database.scaleway.databases.Instance")
    @patch("infra.components.database.pulumi_helpers.handle_error")
    def test_create_error_handling(self, mock_handle_error, mock_instance_class, database_instance):
        """Test error handling during database creation."""
        # Make instance creation fail
        mock_instance_class.side_effect = Exception("Test error")

        # Call create method
        database_instance.create()

        # Verify error was handled
        mock_handle_error.assert_called_once()
        error_call_args = mock_handle_error.call_args[0]
        assert isinstance(error_call_args[0], Exception)
        assert "DatabaseInstance.create(test-database)" in str(error_call_args[1])

    def test_create_instance(self, database_instance):
        """Test instance creation method."""
        with patch("infra.components.database.scaleway.databases.Instance") as mock_instance_class:
            mock_instance = MagicMock()
            mock_instance_class.return_value = mock_instance

            with patch("infra.components.database.pulumi.Config") as mock_config_class:
                mock_config = MagicMock()
                mock_config.require_secret.return_value = "test-password"
                mock_config_class.return_value = mock_config

                database_instance._create_instance()

            # Verify instance creation with correct parameters
            mock_instance_class.assert_called_once()
            call_args = mock_instance_class.call_args
            assert call_args[0][0] == "test-database-instance"
            assert call_args[1]["name"] == "test-database-db-dev"
            assert call_args[1]["engine"] == "PostgreSQL-15"
            assert call_args[1]["node_type"] == "DB-DEV-S"
            assert call_args[1]["is_ha_cluster"] is False
            assert call_args[1]["project_id"] == "test-project-123"
            assert call_args[1]["region"] == "fr-par"
            assert call_args[1]["private_network"] is None
            assert call_args[1]["opts"] == database_instance.opts

    def test_create_instance_with_high_availability(self, database_instance):
        """Test instance creation with high availability enabled."""
        database_instance.config.enable_high_availability = True

        with patch("infra.components.database.scaleway.databases.Instance") as mock_instance_class:
            mock_instance = MagicMock()
            mock_instance_class.return_value = mock_instance

            with patch("infra.components.database.pulumi.Config") as mock_config_class:
                mock_config = MagicMock()
                mock_config.require_secret.return_value = "test-password"
                mock_config_class.return_value = mock_config

                database_instance._create_instance()

            # Verify HA is enabled
            instance_args = mock_instance_class.call_args[1]
            assert instance_args["is_ha_cluster"] is True
            assert instance_args["node_type"] == "DB-DEV-S"

    def test_create_database_without_instance(self, database_instance):
        """Test that database creation fails without instance."""
        with pytest.raises(ValueError, match="Instance must be created before database"):
            database_instance._create_database()

    def test_create_database_success(self, database_instance):
        """Test successful database creation."""
        # Mock instance
        mock_instance = MagicMock()
        mock_instance.id = "test-instance-id"
        database_instance.instance = mock_instance

        with patch("infra.components.database.scaleway.databases.Database") as mock_database_class:
            mock_database = MagicMock()
            mock_database_class.return_value = mock_database

            database_instance._create_database()

            # Verify database creation with correct parameters
            mock_database_class.assert_called_once_with(
                "test-database-database",
                instance_id="test-instance-id",
                name="testdb",
                opts=database_instance.opts,
            )

    def test_get_outputs_empty(self, database_instance):
        """Test get_outputs returns empty dict when instance not created."""
        outputs = database_instance.get_outputs()
        assert outputs == {}

    def test_get_outputs_success(self, database_instance):
        """Test get_outputs returns correct data when instance created."""
        # Mock instance
        mock_instance = MagicMock()
        mock_instance.id = "test-instance-id"
        mock_instance.endpoint_ip = "192.168.1.100"
        mock_instance.endpoint_port = 5432
        database_instance.instance = mock_instance

        outputs = database_instance.get_outputs()

        # Check that outputs contain expected keys and values
        assert outputs["instance_id"] == "test-instance-id"
        assert outputs["endpoint_ip"] == "192.168.1.100"
        assert outputs["endpoint_port"] == 5432
        assert outputs["database_name"] == "testdb"
        assert outputs["username"] == "testuser"
        assert outputs["engine"] == "PostgreSQL-15"
        assert outputs["private_network_enabled"] is False

    def test_get_connection_string_not_created(self, database_instance):
        """Test get_connection_string raises error when instance not created."""
        with pytest.raises(ValueError, match="Instance not created yet"):
            database_instance.get_connection_string()

    def test_get_connection_string_success(self, database_instance):
        """Test get_connection_string returns correct connection string."""
        # Mock instance
        mock_instance = MagicMock()
        mock_instance.endpoint_ip = "192.168.1.100"
        mock_instance.endpoint_port = 5432
        database_instance.instance = mock_instance

        connection_string = database_instance.get_connection_string()

        # Should be a pulumi.Output.concat object
        assert connection_string is not None

    def test_get_instance_id_not_created(self, database_instance):
        """Test get_instance_id raises error when instance not created."""
        with pytest.raises(ValueError, match="Instance not created yet"):
            database_instance.get_instance_id()

    def test_get_instance_id_success(self, database_instance):
        """Test get_instance_id returns instance ID."""
        mock_instance = MagicMock()
        mock_instance.id = "test-instance-id"
        database_instance.instance = mock_instance

        instance_id = database_instance.get_instance_id()
        assert instance_id == "test-instance-id"

    def test_repr(self, database_instance):
        """Test string representation of DatabaseInstance."""
        expected = "DatabaseInstance(name=test-database, environment=dev)"
        assert repr(database_instance) == expected

    def test_different_engines(self):
        """Test database instance with different engine versions."""
        config = DatabaseConfig(engine="PostgreSQL-14")
        db = DatabaseInstance(
            name="pg14-database",
            environment="dev",
            config=config,
            project_id="test-project-123",
        )

        with patch("infra.components.database.scaleway.databases.Instance") as mock_instance_class:
            mock_instance = MagicMock()
            mock_instance_class.return_value = mock_instance

            with patch("infra.components.database.pulumi.Config") as mock_config_class:
                mock_config = MagicMock()
                mock_config.require_secret.return_value = "test-password"
                mock_config_class.return_value = mock_config

                db._create_instance()

            # Verify engine is set correctly
            instance_args = mock_instance_class.call_args[1]
            assert instance_args["engine"] == "PostgreSQL-14"
            assert instance_args["node_type"] == "DB-DEV-S"

    def test_backup_disabled(self):
        """Test database instance with backups disabled."""
        config = DatabaseConfig(enable_backups=False)
        db = DatabaseInstance(
            name="no-backup-db",
            environment="dev",
            config=config,
            project_id="test-project-123",
        )

        with patch("infra.components.database.scaleway.databases.Instance") as mock_instance_class:
            mock_instance = MagicMock()
            mock_instance_class.return_value = mock_instance

            with patch("infra.components.database.pulumi.Config") as mock_config_class:
                mock_config = MagicMock()
                mock_config.require_secret.return_value = "test-password"
                mock_config_class.return_value = mock_config

                db._create_instance()

            # Verify instance was created with correct node type
            instance_args = mock_instance_class.call_args[1]
            assert instance_args["node_type"] == "DB-DEV-S"
            assert instance_args["engine"] == "PostgreSQL-15"


class TestDatabaseSecretManagerIntegration:
    """Tests for DatabaseInstance integration with SecretManager."""

    @pytest.fixture
    def secret_configs(self):
        """Create secret configurations including database password."""
        return [
            SecretConfig(
                name="db-password",
                description="Database password",
                data="secret-from-manager",
                path="/database",
            ),
        ]

    @pytest.fixture
    def secret_manager(self, secret_configs):
        """Create a SecretManager instance for testing."""
        return SecretManager(
            name="test-secrets",
            environment="dev",
            configs=secret_configs,
            project_id="test-project-123",
            region="fr-par",
        )

    @pytest.fixture
    def database_config(self):
        """Create a valid database configuration for testing."""
        return DatabaseConfig(
            engine="PostgreSQL-15",
            volume_size=50,
            backup_retention_days=14,
            user_name="testuser",
            database_name="testdb",
        )

    def test_database_with_secret_manager_initialization(self, database_config, secret_manager):
        """Test DatabaseInstance initializes correctly with SecretManager."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            secret_manager=secret_manager,
            password_secret_name="db-password",
        )

        assert db.secret_manager is secret_manager
        assert db.password_secret_name == "db-password"

    def test_database_secret_manager_without_secret_name_raises(self, database_config, secret_manager):
        """Test that providing secret_manager without password_secret_name raises error."""
        with pytest.raises(ValueError, match="password_secret_name is required"):
            DatabaseInstance(
                name="test-database",
                environment="dev",
                config=database_config,
                project_id="test-project-123",
                secret_manager=secret_manager,
                # Missing password_secret_name
            )

    def test_database_secret_name_without_manager_raises(self, database_config):
        """Test that providing password_secret_name without secret_manager raises error."""
        with pytest.raises(ValueError, match="secret_manager is required"):
            DatabaseInstance(
                name="test-database",
                environment="dev",
                config=database_config,
                project_id="test-project-123",
                password_secret_name="db-password",
                # Missing secret_manager
            )

    def test_get_password_from_secret_manager(self, database_config, secret_manager):
        """Test _get_password retrieves password from SecretManager."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            secret_manager=secret_manager,
            password_secret_name="db-password",
        )

        password = db._get_password()
        assert password == "secret-from-manager"

    def test_get_password_from_pulumi_config(self, database_config):
        """Test _get_password falls back to Pulumi config when no SecretManager."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
        )

        with patch("infra.components.database.pulumi.Config") as mock_config_class:
            mock_config = MagicMock()
            mock_config.require_secret.return_value = "pulumi-config-password"
            mock_config_class.return_value = mock_config

            password = db._get_password()

            assert password == "pulumi-config-password"
            mock_config.require_secret.assert_called_once_with("db_password")

    @patch("infra.components.database.scaleway.databases.Instance")
    def test_create_instance_uses_secret_manager_password(
        self, mock_instance_class, database_config, secret_manager
    ):
        """Test that _create_instance uses password from SecretManager."""
        mock_instance = MagicMock()
        mock_instance_class.return_value = mock_instance

        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            secret_manager=secret_manager,
            password_secret_name="db-password",
        )

        db._create_instance()

        # Verify instance was created with password from SecretManager
        mock_instance_class.assert_called_once()
        call_kwargs = mock_instance_class.call_args[1]
        assert call_kwargs["password"] == "secret-from-manager"

    def test_get_password_invalid_secret_name_raises(self, database_config, secret_manager):
        """Test _get_password raises KeyError for invalid secret name."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            secret_manager=secret_manager,
            password_secret_name="nonexistent-secret",
        )

        with pytest.raises(KeyError, match="nonexistent-secret"):
            db._get_password()


class TestDatabasePrivateNetworkIntegration:
    """Tests for DatabaseInstance integration with PrivateNetwork."""

    @pytest.fixture
    def database_config(self):
        """Create a valid database configuration for testing."""
        return DatabaseConfig(
            engine="PostgreSQL-15",
            volume_size=50,
            backup_retention_days=14,
            user_name="testuser",
            database_name="testdb",
        )

    @pytest.fixture
    def mock_private_network(self):
        """Create a mock PrivateNetwork instance."""
        pn = MagicMock()
        pn.name = "test-private-network"
        pn.is_enabled.return_value = True
        pn.get_private_network_id.return_value = "pn-12345"
        return pn

    @pytest.fixture
    def mock_disabled_private_network(self):
        """Create a mock disabled PrivateNetwork instance."""
        pn = MagicMock()
        pn.name = "disabled-private-network"
        pn.is_enabled.return_value = False
        return pn

    def test_database_with_private_network_initialization(self, database_config, mock_private_network):
        """Test DatabaseInstance initializes correctly with PrivateNetwork."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
        )

        assert db.private_network is mock_private_network
        assert db.private_network_ip is None

    def test_database_with_private_network_and_static_ip(self, database_config, mock_private_network):
        """Test DatabaseInstance initializes with private network and static IP."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
            private_network_ip="172.16.20.4/22",
        )

        assert db.private_network is mock_private_network
        assert db.private_network_ip == "172.16.20.4/22"

    def test_build_private_network_config_none_when_no_network(self, database_config):
        """Test _build_private_network_config returns None when no private network."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
        )

        config = db._build_private_network_config()
        assert config is None

    def test_build_private_network_config_none_when_disabled(
        self, database_config, mock_disabled_private_network
    ):
        """Test _build_private_network_config returns None when network is disabled."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_disabled_private_network,
        )

        config = db._build_private_network_config()
        assert config is None

    @patch("infra.components.database.scaleway.databases.InstancePrivateNetworkArgs")
    def test_build_private_network_config_with_ipam(
        self, mock_pn_args_class, database_config, mock_private_network
    ):
        """Test _build_private_network_config with IPAM mode (no static IP)."""
        mock_pn_args = MagicMock()
        mock_pn_args_class.return_value = mock_pn_args

        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
        )

        config = db._build_private_network_config()

        mock_pn_args_class.assert_called_once_with(
            pn_id="pn-12345",
            enable_ipam=True,
        )
        assert config is mock_pn_args

    @patch("infra.components.database.scaleway.databases.InstancePrivateNetworkArgs")
    def test_build_private_network_config_with_static_ip(
        self, mock_pn_args_class, database_config, mock_private_network
    ):
        """Test _build_private_network_config with static IP mode."""
        mock_pn_args = MagicMock()
        mock_pn_args_class.return_value = mock_pn_args

        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
            private_network_ip="172.16.20.4/22",
        )

        config = db._build_private_network_config()

        mock_pn_args_class.assert_called_once_with(
            pn_id="pn-12345",
            ip_net="172.16.20.4/22",
        )
        assert config is mock_pn_args

    @patch("infra.components.database.scaleway.databases.Instance")
    def test_create_instance_with_private_network(
        self, mock_instance_class, database_config, mock_private_network
    ):
        """Test _create_instance includes private network configuration."""
        mock_instance = MagicMock()
        mock_instance_class.return_value = mock_instance

        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
        )

        with patch("infra.components.database.pulumi.Config") as mock_config_class:
            mock_config = MagicMock()
            mock_config.require_secret.return_value = "test-password"
            mock_config_class.return_value = mock_config

            db._create_instance()

        # Verify instance was created with private_network parameter
        mock_instance_class.assert_called_once()
        call_kwargs = mock_instance_class.call_args[1]
        assert "private_network" in call_kwargs
        assert call_kwargs["private_network"] is not None

    @patch("infra.components.database.scaleway.databases.Instance")
    def test_create_instance_without_private_network(self, mock_instance_class, database_config):
        """Test _create_instance without private network configuration."""
        mock_instance = MagicMock()
        mock_instance_class.return_value = mock_instance

        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
        )

        with patch("infra.components.database.pulumi.Config") as mock_config_class:
            mock_config = MagicMock()
            mock_config.require_secret.return_value = "test-password"
            mock_config_class.return_value = mock_config

            db._create_instance()

        # Verify instance was created with private_network=None
        mock_instance_class.assert_called_once()
        call_kwargs = mock_instance_class.call_args[1]
        assert call_kwargs["private_network"] is None

    def test_is_private_network_enabled_true(self, database_config, mock_private_network):
        """Test is_private_network_enabled returns True when configured."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
        )

        assert db.is_private_network_enabled() is True

    def test_is_private_network_enabled_false_no_network(self, database_config):
        """Test is_private_network_enabled returns False when not configured."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
        )

        assert db.is_private_network_enabled() is False

    def test_is_private_network_enabled_false_disabled(self, database_config, mock_disabled_private_network):
        """Test is_private_network_enabled returns False when network is disabled."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_disabled_private_network,
        )

        assert db.is_private_network_enabled() is False

    def test_get_private_network_connection_string_not_created(self, database_config, mock_private_network):
        """Test get_private_network_connection_string raises error when instance not created."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
        )

        with pytest.raises(ValueError, match="Instance not created yet"):
            db.get_private_network_connection_string()

    def test_get_private_network_connection_string_no_network(self, database_config):
        """Test get_private_network_connection_string raises error when no private network."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
        )

        # Mock instance as created
        db.instance = MagicMock()

        with pytest.raises(ValueError, match="Private network not configured"):
            db.get_private_network_connection_string()

    def test_get_private_network_host_not_created(self, database_config, mock_private_network):
        """Test get_private_network_host raises error when instance not created."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
        )

        with pytest.raises(ValueError, match="Instance not created yet"):
            db.get_private_network_host()

    def test_get_private_network_port_not_created(self, database_config, mock_private_network):
        """Test get_private_network_port raises error when instance not created."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
        )

        with pytest.raises(ValueError, match="Instance not created yet"):
            db.get_private_network_port()

    def test_get_outputs_includes_private_network_info(self, database_config, mock_private_network):
        """Test get_outputs includes private network information when configured."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
        )

        # Mock instance with private network endpoint
        mock_instance = MagicMock()
        mock_instance.id = "instance-123"
        mock_instance.endpoint_ip = "1.2.3.4"
        mock_instance.endpoint_port = 5432
        mock_instance.private_network.hostname = "db.private.local"
        mock_instance.private_network.ip = "172.16.20.4"
        mock_instance.private_network.port = 5432
        mock_instance.private_network.pn_id = "pn-12345"
        db.instance = mock_instance

        outputs = db.get_outputs()

        assert outputs["private_network_enabled"] is True
        assert "private_network_endpoint" in outputs
        assert outputs["private_network_endpoint"]["hostname"] == "db.private.local"
        assert outputs["private_network_endpoint"]["ip"] == "172.16.20.4"
        assert outputs["private_network_endpoint"]["port"] == 5432
        assert outputs["private_network_endpoint"]["pn_id"] == "pn-12345"

    def test_get_outputs_no_private_network(self, database_config):
        """Test get_outputs when private network is not configured."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
        )

        # Mock instance
        mock_instance = MagicMock()
        mock_instance.id = "instance-123"
        mock_instance.endpoint_ip = "1.2.3.4"
        mock_instance.endpoint_port = 5432
        db.instance = mock_instance

        outputs = db.get_outputs()

        assert outputs["private_network_enabled"] is False
        assert "private_network_endpoint" not in outputs

    def test_get_connection_string_with_private_network_flag(self, database_config, mock_private_network):
        """Test get_connection_string with use_private_network=True."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config,
            project_id="test-project-123",
            private_network=mock_private_network,
        )

        # Mock instance with private network endpoint
        mock_instance = MagicMock()
        mock_instance.private_network.hostname = "db.private.local"
        mock_instance.private_network.port = 5432
        db.instance = mock_instance

        # Should not raise when use_private_network=True
        connection_string = db.get_connection_string(use_private_network=True)
        assert connection_string is not None


class TestDatabaseEncryptionConfiguration:
    """Tests for DatabaseInstance encryption at rest configuration."""

    @pytest.fixture
    def database_config_encrypted(self):
        """Create a database configuration with encryption enabled."""
        return DatabaseConfig(
            engine="PostgreSQL-15",
            volume_size=50,
            enable_encryption_at_rest=True,
            user_name="testuser",
            database_name="testdb",
        )

    @pytest.fixture
    def database_config_unencrypted(self):
        """Create a database configuration with encryption disabled."""
        return DatabaseConfig(
            engine="PostgreSQL-15",
            volume_size=50,
            enable_encryption_at_rest=False,
            user_name="testuser",
            database_name="testdb",
        )

    def test_encryption_enabled_by_default(self):
        """Test that encryption at rest is enabled by default."""
        config = DatabaseConfig()
        assert config.enable_encryption_at_rest is True

    def test_encryption_can_be_disabled(self):
        """Test that encryption at rest can be explicitly disabled."""
        config = DatabaseConfig(enable_encryption_at_rest=False)
        assert config.enable_encryption_at_rest is False

    @patch("infra.components.database.scaleway.databases.Instance")
    def test_create_instance_with_encryption_enabled(self, mock_instance_class, database_config_encrypted):
        """Test that _create_instance passes encryption_at_rest=True."""
        mock_instance = MagicMock()
        mock_instance_class.return_value = mock_instance

        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config_encrypted,
            project_id="test-project-123",
        )

        with patch("infra.components.database.pulumi.Config") as mock_config_class:
            mock_config = MagicMock()
            mock_config.require_secret.return_value = "test-password"
            mock_config_class.return_value = mock_config

            db._create_instance()

        # Verify encryption_at_rest is passed to instance creation
        mock_instance_class.assert_called_once()
        call_kwargs = mock_instance_class.call_args[1]
        assert call_kwargs["encryption_at_rest"] is True

    @patch("infra.components.database.scaleway.databases.Instance")
    def test_create_instance_with_encryption_disabled(self, mock_instance_class, database_config_unencrypted):
        """Test that _create_instance passes encryption_at_rest=False."""
        mock_instance = MagicMock()
        mock_instance_class.return_value = mock_instance

        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config_unencrypted,
            project_id="test-project-123",
        )

        with patch("infra.components.database.pulumi.Config") as mock_config_class:
            mock_config = MagicMock()
            mock_config.require_secret.return_value = "test-password"
            mock_config_class.return_value = mock_config

            db._create_instance()

        # Verify encryption_at_rest is passed to instance creation
        mock_instance_class.assert_called_once()
        call_kwargs = mock_instance_class.call_args[1]
        assert call_kwargs["encryption_at_rest"] is False

    def test_get_outputs_includes_encryption_status(self, database_config_encrypted):
        """Test that get_outputs includes encryption_at_rest_enabled."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config_encrypted,
            project_id="test-project-123",
        )

        # Mock instance
        mock_instance = MagicMock()
        mock_instance.id = "instance-123"
        mock_instance.endpoint_ip = "1.2.3.4"
        mock_instance.endpoint_port = 5432
        db.instance = mock_instance

        outputs = db.get_outputs()

        assert "encryption_at_rest_enabled" in outputs
        assert outputs["encryption_at_rest_enabled"] is True

    def test_get_outputs_encryption_disabled(self, database_config_unencrypted):
        """Test that get_outputs shows encryption disabled when configured."""
        db = DatabaseInstance(
            name="test-database",
            environment="dev",
            config=database_config_unencrypted,
            project_id="test-project-123",
        )

        # Mock instance
        mock_instance = MagicMock()
        mock_instance.id = "instance-123"
        mock_instance.endpoint_ip = "1.2.3.4"
        mock_instance.endpoint_port = 5432
        db.instance = mock_instance

        outputs = db.get_outputs()

        assert "encryption_at_rest_enabled" in outputs
        assert outputs["encryption_at_rest_enabled"] is False
