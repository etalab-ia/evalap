"""Unit tests for SecretManager component."""

from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from infra.components.secret_manager import SecretManager
from infra.config.models import SecretConfig


class TestSecretConfig:
    """Tests for SecretConfig model."""

    def test_secret_config_valid(self):
        """Test valid SecretConfig creation."""
        config = SecretConfig(
            name="my-secret",
            description="Test secret",
            data="secret-value",
            path="/app/secrets",
        )
        assert config.name == "my-secret"
        assert config.description == "Test secret"
        assert config.data == "secret-value"
        assert config.path == "/app/secrets"
        assert config.protected is False

    def test_secret_config_minimal(self):
        """Test SecretConfig with minimal required fields."""
        config = SecretConfig(name="minimal-secret", data="value")
        assert config.name == "minimal-secret"
        assert config.data == "value"
        assert config.path == "/"
        assert config.description is None
        assert config.secret_type is None

    def test_secret_config_invalid_name_uppercase(self):
        """Test that uppercase letters in name raise validation error."""
        with pytest.raises(ValidationError) as exc_info:
            SecretConfig(name="MySecret", data="value")
        assert "must match pattern" in str(exc_info.value)

    def test_secret_config_invalid_name_starts_with_number(self):
        """Test that name starting with number raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            SecretConfig(name="1secret", data="value")
        assert "must match pattern" in str(exc_info.value)

    def test_secret_config_invalid_name_special_chars(self):
        """Test that special characters in name raise validation error."""
        with pytest.raises(ValidationError) as exc_info:
            SecretConfig(name="my_secret", data="value")  # underscore not allowed
        assert "must match pattern" in str(exc_info.value)

    def test_secret_config_with_type(self):
        """Test SecretConfig with secret type."""
        config = SecretConfig(
            name="db-creds",
            data='{"username": "admin", "password": "secret"}',
            secret_type="database_credentials",
        )
        assert config.secret_type == "database_credentials"


class TestSecretManager:
    """Tests for SecretManager component."""

    @pytest.fixture
    def secret_configs(self):
        """Create valid secret configurations for testing."""
        return [
            SecretConfig(
                name="db-password",
                description="Database password",
                data="super-secret-password",
                path="/database",
            ),
            SecretConfig(
                name="api-key",
                description="External API key",
                data="api-key-12345",
                path="/external",
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
            tags={"team": "platform"},
        )

    def test_secret_manager_initialization(self, secret_manager, secret_configs):
        """Test that SecretManager initializes correctly."""
        assert secret_manager.name == "test-secrets"
        assert secret_manager.environment == "dev"
        assert secret_manager.configs == secret_configs
        assert secret_manager.project_id == "test-project-123"
        assert secret_manager.region == "fr-par"
        assert secret_manager.tags == {"team": "platform"}
        assert secret_manager.secrets == {}
        assert secret_manager.versions == {}

    def test_secret_manager_initialization_with_defaults(self):
        """Test SecretManager initialization with minimal parameters."""
        configs = [SecretConfig(name="simple-secret", data="value")]
        sm = SecretManager(
            name="minimal-secrets",
            environment="staging",
            configs=configs,
            project_id="test-project-456",
        )

        assert sm.name == "minimal-secrets"
        assert sm.environment == "staging"
        assert sm.region == "fr-par"  # Default value
        assert sm.tags == {}  # Default empty dict

    def test_format_tags_list(self, secret_manager):
        """Test that tags are formatted correctly as a list."""
        tags_list = secret_manager._format_tags_list()

        assert "environment:dev" in tags_list
        assert "component:test-secrets" in tags_list
        assert "managed-by:pulumi" in tags_list
        assert "team:platform" in tags_list

    @patch("infra.components.secret_manager.scaleway.secrets.Secret")
    @patch("infra.components.secret_manager.scaleway.secrets.Version")
    @patch("infra.components.secret_manager.pulumi_helpers.log_resource_creation")
    def test_create_success(
        self,
        mock_log,
        mock_version_class,
        mock_secret_class,
        secret_manager,
    ):
        """Test successful creation of secrets."""
        # Mock the secret and version objects
        mock_secret = MagicMock()
        mock_secret.id = "secret-id-123"
        mock_secret_class.return_value = mock_secret

        mock_version = MagicMock()
        mock_version.id = "version-id-456"
        mock_version_class.return_value = mock_version

        # Call create
        secret_manager.create()

        # Verify log was called
        mock_log.assert_called_once()

        # Verify secrets were created (2 secrets)
        assert mock_secret_class.call_count == 2
        assert mock_version_class.call_count == 2

        # Verify secrets are tracked
        assert len(secret_manager.secrets) == 2
        assert "db-password" in secret_manager.secrets
        assert "api-key" in secret_manager.secrets

    @patch("infra.components.secret_manager.scaleway.secrets.Secret")
    @patch("infra.components.secret_manager.scaleway.secrets.Version")
    @patch("infra.components.secret_manager.pulumi_helpers.log_resource_creation")
    def test_get_outputs(
        self,
        mock_log,
        mock_version_class,
        mock_secret_class,
        secret_manager,
    ):
        """Test get_outputs returns correct structure."""
        # Mock the secret and version objects
        mock_secret1 = MagicMock()
        mock_secret1.id = "secret-id-1"
        mock_secret2 = MagicMock()
        mock_secret2.id = "secret-id-2"
        mock_secret_class.side_effect = [mock_secret1, mock_secret2]

        mock_version = MagicMock()
        mock_version.id = "version-id"
        mock_version_class.return_value = mock_version

        # Create secrets
        secret_manager.create()

        # Get outputs
        outputs = secret_manager.get_outputs()

        assert "secrets" in outputs
        assert "secret_count" in outputs
        assert "region" in outputs
        assert outputs["secret_count"] == 2
        assert outputs["region"] == "fr-par"

    @patch("infra.components.secret_manager.scaleway.secrets.Secret")
    @patch("infra.components.secret_manager.scaleway.secrets.Version")
    @patch("infra.components.secret_manager.pulumi_helpers.log_resource_creation")
    def test_get_secret_id(
        self,
        mock_log,
        mock_version_class,
        mock_secret_class,
        secret_manager,
    ):
        """Test get_secret_id returns correct ID."""
        mock_secret = MagicMock()
        mock_secret.id = "secret-id-123"
        mock_secret_class.return_value = mock_secret

        mock_version = MagicMock()
        mock_version_class.return_value = mock_version

        secret_manager.create()

        secret_id = secret_manager.get_secret_id("db-password")
        assert secret_id == "secret-id-123"

    @patch("infra.components.secret_manager.scaleway.secrets.Secret")
    @patch("infra.components.secret_manager.scaleway.secrets.Version")
    @patch("infra.components.secret_manager.pulumi_helpers.log_resource_creation")
    def test_get_secret_id_not_found(
        self,
        mock_log,
        mock_version_class,
        mock_secret_class,
        secret_manager,
    ):
        """Test get_secret_id raises KeyError for unknown secret."""
        mock_secret = MagicMock()
        mock_secret_class.return_value = mock_secret

        mock_version = MagicMock()
        mock_version_class.return_value = mock_version

        secret_manager.create()

        with pytest.raises(KeyError) as exc_info:
            secret_manager.get_secret_id("nonexistent-secret")
        assert "nonexistent-secret" in str(exc_info.value)

    @patch("infra.components.secret_manager.scaleway.secrets.Secret")
    @patch("infra.components.secret_manager.scaleway.secrets.Version")
    @patch("infra.components.secret_manager.pulumi_helpers.log_resource_creation")
    def test_get_secret_for_container(
        self,
        mock_log,
        mock_version_class,
        mock_secret_class,
        secret_manager,
    ):
        """Test get_secret_for_container returns correct format."""
        mock_secret = MagicMock()
        mock_secret.id = "secret-id-123"
        mock_secret_class.return_value = mock_secret

        mock_version = MagicMock()
        mock_version_class.return_value = mock_version

        secret_manager.create()

        container_secret = secret_manager.get_secret_for_container("db-password", "DATABASE_PASSWORD")

        assert container_secret["key"] == "DATABASE_PASSWORD"
        assert container_secret["secret_id"] == "secret-id-123"
        assert container_secret["secret_version"] == "latest"

    def test_get_outputs_empty(self, secret_manager):
        """Test get_outputs before create returns empty secrets."""
        outputs = secret_manager.get_outputs()
        assert outputs["secrets"] == {}
        assert outputs["secret_count"] == 0


class TestSecretValidation:
    """Tests for secret validation utilities."""

    def test_validate_secret_name_valid(self):
        """Test valid secret names pass validation."""
        from infra.utils.scaleway_helpers import validate_secret_name

        assert validate_secret_name("my-secret") is True
        assert validate_secret_name("db-password-123") is True
        assert validate_secret_name("a") is True
        assert validate_secret_name("api-key") is True

    def test_validate_secret_name_invalid(self):
        """Test invalid secret names raise ValueError."""
        from infra.utils.scaleway_helpers import validate_secret_name

        with pytest.raises(ValueError):
            validate_secret_name("MySecret")  # uppercase

        with pytest.raises(ValueError):
            validate_secret_name("1secret")  # starts with number

        with pytest.raises(ValueError):
            validate_secret_name("my_secret")  # underscore

        with pytest.raises(ValueError):
            validate_secret_name("")  # empty

    def test_validate_secret_path_valid(self):
        """Test valid secret paths pass validation."""
        from infra.utils.scaleway_helpers import validate_secret_path

        assert validate_secret_path("/") is True
        assert validate_secret_path("/app") is True
        assert validate_secret_path("/app/secrets") is True
        assert validate_secret_path("/my-app/db_creds") is True

    def test_validate_secret_path_invalid(self):
        """Test invalid secret paths raise ValueError."""
        from infra.utils.scaleway_helpers import validate_secret_path

        with pytest.raises(ValueError):
            validate_secret_path("")  # empty

        with pytest.raises(ValueError):
            validate_secret_path("app/secrets")  # doesn't start with /

        with pytest.raises(ValueError):
            validate_secret_path("/app/secrets!")  # special char

    def test_validate_secret_config_valid(self):
        """Test valid secret config passes validation."""
        from infra.utils.validation import validate_secret_config

        config = SecretConfig(
            name="valid-secret",
            data="secret-value",
            path="/app",
        )
        assert validate_secret_config(config) is True

    def test_validate_secret_config_invalid_type(self):
        """Test invalid secret type raises ValueError."""
        from infra.utils.validation import validate_secret_config

        config = SecretConfig(
            name="valid-secret",
            data="secret-value",
            secret_type="invalid_type",
        )
        with pytest.raises(ValueError) as exc_info:
            validate_secret_config(config)
        assert "Invalid secret type" in str(exc_info.value)


class TestSecretManagerContainerIntegration:
    """Tests for SecretManager container integration methods."""

    @pytest.fixture
    def secret_configs(self):
        """Create valid secret configurations for testing."""
        return [
            SecretConfig(
                name="db-password",
                description="Database password",
                data="super-secret-password",
                path="/database",
            ),
            SecretConfig(
                name="api-key",
                description="External API key",
                data="api-key-12345",
                path="/external",
            ),
            SecretConfig(
                name="jwt-secret",
                description="JWT signing secret",
                data="jwt-secret-value",
                path="/auth",
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

    def test_get_secrets_for_container_single(self, secret_manager):
        """Test getting a single secret for container."""
        result = secret_manager.get_secrets_for_container(
            {
                "db-password": "DATABASE_PASSWORD",
            }
        )

        assert result == {"DATABASE_PASSWORD": "super-secret-password"}

    def test_get_secrets_for_container_multiple(self, secret_manager):
        """Test getting multiple secrets for container."""
        result = secret_manager.get_secrets_for_container(
            {
                "db-password": "DATABASE_PASSWORD",
                "api-key": "API_KEY",
                "jwt-secret": "JWT_SECRET",
            }
        )

        assert result == {
            "DATABASE_PASSWORD": "super-secret-password",
            "API_KEY": "api-key-12345",
            "JWT_SECRET": "jwt-secret-value",
        }

    def test_get_secrets_for_container_missing_secret(self, secret_manager):
        """Test getting secrets with missing secret name."""
        result = secret_manager.get_secrets_for_container(
            {
                "db-password": "DATABASE_PASSWORD",
                "nonexistent": "MISSING_VAR",
            }
        )

        # Only existing secret should be in result
        assert result == {"DATABASE_PASSWORD": "super-secret-password"}
        assert "MISSING_VAR" not in result

    def test_get_secrets_for_container_empty_mappings(self, secret_manager):
        """Test getting secrets with empty mappings."""
        result = secret_manager.get_secrets_for_container({})
        assert result == {}

    def test_get_config_by_name_found(self, secret_manager):
        """Test _get_config_by_name returns config when found."""
        config = secret_manager._get_config_by_name("db-password")

        assert config is not None
        assert config.name == "db-password"
        assert config.data == "super-secret-password"

    def test_get_config_by_name_not_found(self, secret_manager):
        """Test _get_config_by_name returns None when not found."""
        config = secret_manager._get_config_by_name("nonexistent")
        assert config is None

    def test_get_secret_data_success(self, secret_manager):
        """Test get_secret_data returns correct secret value."""
        data = secret_manager.get_secret_data("db-password")
        assert data == "super-secret-password"

    def test_get_secret_data_different_secret(self, secret_manager):
        """Test get_secret_data works for different secrets."""
        data = secret_manager.get_secret_data("api-key")
        assert data == "api-key-12345"

    def test_get_secret_data_not_found(self, secret_manager):
        """Test get_secret_data raises KeyError for unknown secret."""
        with pytest.raises(KeyError) as exc_info:
            secret_manager.get_secret_data("nonexistent-secret")
        assert "nonexistent-secret" in str(exc_info.value)
        assert "not found in configs" in str(exc_info.value)
