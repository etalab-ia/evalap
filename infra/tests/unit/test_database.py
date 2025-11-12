"""Unit tests for DatabaseInstance component."""

from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from infra.components.database import DatabaseInstance
from infra.config.models import DatabaseConfig


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

    @patch("infra.components.database.scaleway.DatabaseInstance")
    @patch("infra.components.database.scaleway.Database")
    @patch("infra.components.database.scaleway.DatabaseUser")
    @patch("infra.components.database.pulumi_helpers.log_resource_creation")
    def test_create_success(
        self, mock_log, mock_user_class, mock_database_class, mock_instance_class, database_instance
    ):
        """Test successful creation of database infrastructure."""
        # Mock the instance, database, and user objects
        mock_instance = MagicMock()
        mock_database = MagicMock()
        mock_user = MagicMock()
        mock_instance_class.return_value = mock_instance
        mock_database_class.return_value = mock_database
        mock_user_class.return_value = mock_user

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
        assert instance_args["node_type"] == "db-dev-s"
        assert instance_args["is_ha_cluster"] is False
        assert instance_args["volume_size_gb"] == 50
        assert instance_args["backup_schedule_frequency"] == "daily"
        assert instance_args["backup_schedule_retention_days"] == 14
        assert instance_args["auto_backup_enabled"] is True
        assert instance_args["project_id"] == "test-project-123"
        assert instance_args["region"] == "fr-par"

        # Verify database was created
        mock_database_class.assert_called_once()
        database_args = mock_database_class.call_args[1]
        assert database_args["name"] == "testdb"

        # Verify user was created
        mock_user_class.assert_called_once()
        user_args = mock_user_class.call_args[1]
        assert user_args["name"] == "testuser"
        assert user_args["is_admin"] is True

    @patch("infra.components.database.scaleway.DatabaseInstance")
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
        with patch("infra.components.database.scaleway.DatabaseInstance") as mock_instance_class:
            mock_instance = MagicMock()
            mock_instance_class.return_value = mock_instance

            database_instance._create_instance()

            # Verify instance creation with correct parameters
            mock_instance_class.assert_called_once()
            call_args = mock_instance_class.call_args
            assert call_args[0][0] == "test-database-instance"
            assert call_args[1]["name"] == "test-database-db-dev"
            assert call_args[1]["engine"] == "PostgreSQL-15"
            assert call_args[1]["node_type"] == "db-dev-s"
            assert call_args[1]["is_ha_cluster"] is False
            assert call_args[1]["volume_size_gb"] == 50
            assert call_args[1]["backup_schedule_frequency"] == "daily"
            assert call_args[1]["backup_schedule_retention_days"] == 14
            assert call_args[1]["auto_backup_enabled"] is True
            assert call_args[1]["project_id"] == "test-project-123"
            assert call_args[1]["region"] == "fr-par"
            assert isinstance(call_args[1]["tags"], dict)
            assert call_args[1]["opts"] == database_instance.opts

    def test_create_instance_with_high_availability(self, database_instance):
        """Test instance creation with high availability enabled."""
        database_instance.config.enable_high_availability = True

        with patch("infra.components.database.scaleway.DatabaseInstance") as mock_instance_class:
            mock_instance = MagicMock()
            mock_instance_class.return_value = mock_instance

            database_instance._create_instance()

            # Verify HA is enabled
            instance_args = mock_instance_class.call_args[1]
            assert instance_args["is_ha_cluster"] is True

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

        with patch("infra.components.database.scaleway.Database") as mock_database_class:
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

    def test_create_user_without_instance(self, database_instance):
        """Test that user creation fails without instance."""
        with pytest.raises(ValueError, match="Instance must be created before user"):
            database_instance._create_user()

    def test_create_user_success(self, database_instance):
        """Test successful user creation."""
        # Mock instance
        mock_instance = MagicMock()
        mock_instance.id = "test-instance-id"
        database_instance.instance = mock_instance

        with patch("infra.components.database.scaleway.DatabaseUser") as mock_user_class:
            mock_user = MagicMock()
            mock_user_class.return_value = mock_user

            # Mock config
            with patch("infra.components.database.pulumi.Config") as mock_config_class:
                mock_config = MagicMock()
                mock_config.require_secret.return_value = "secret-password"
                mock_config_class.return_value = mock_config

                database_instance._create_user()

            # Verify user creation with correct parameters
            mock_user_class.assert_called_once_with(
                "test-database-user",
                instance_id="test-instance-id",
                name="testuser",
                password="secret-password",
                is_admin=True,
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
        assert outputs["host"] == "192.168.1.100"
        assert outputs["port"] == 5432
        assert outputs["database_name"] == "testdb"
        assert outputs["username"] == "testuser"
        assert outputs["engine"] == "PostgreSQL-15"
        assert outputs["volume_size_gb"] == 50
        assert outputs["backup_retention_days"] == 14
        assert "endpoint" in outputs  # pulumi.Output.concat result

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

    def test_get_host_not_created(self, database_instance):
        """Test get_host raises error when instance not created."""
        with pytest.raises(ValueError, match="Instance not created yet"):
            database_instance.get_host()

    def test_get_host_success(self, database_instance):
        """Test get_host returns instance host."""
        mock_instance = MagicMock()
        mock_instance.endpoint_ip = "192.168.1.100"
        database_instance.instance = mock_instance

        host = database_instance.get_host()
        assert host == "192.168.1.100"

    def test_get_port_not_created(self, database_instance):
        """Test get_port raises error when instance not created."""
        with pytest.raises(ValueError, match="Instance not created yet"):
            database_instance.get_port()

    def test_get_port_success(self, database_instance):
        """Test get_port returns instance port."""
        mock_instance = MagicMock()
        mock_instance.endpoint_port = 5432
        database_instance.instance = mock_instance

        port = database_instance.get_port()
        assert port == 5432

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

        with patch("infra.components.database.scaleway.DatabaseInstance") as mock_instance_class:
            mock_instance = MagicMock()
            mock_instance_class.return_value = mock_instance

            db._create_instance()

            # Verify engine is set correctly
            instance_args = mock_instance_class.call_args[1]
            assert instance_args["engine"] == "PostgreSQL-14"

    def test_backup_disabled(self):
        """Test database instance with backups disabled."""
        config = DatabaseConfig(enable_backups=False)
        db = DatabaseInstance(
            name="no-backup-db",
            environment="dev",
            config=config,
            project_id="test-project-123",
        )

        with patch("infra.components.database.scaleway.DatabaseInstance") as mock_instance_class:
            mock_instance = MagicMock()
            mock_instance_class.return_value = mock_instance

            db._create_instance()

            # Verify backups are disabled
            instance_args = mock_instance_class.call_args[1]
            assert instance_args["auto_backup_enabled"] is False
