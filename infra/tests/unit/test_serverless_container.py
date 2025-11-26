"""Unit tests for ServerlessContainer component."""

from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from infra.components.private_network import PrivateNetwork
from infra.components.secret_manager import SecretManager
from infra.components.serverless_container import ServerlessContainer
from infra.config.models import ContainerConfig, NetworkConfig, SecretConfig


class TestServerlessContainer:
    """Tests for ServerlessContainer component."""

    @pytest.fixture
    def container_config(self):
        """Create a valid container configuration for testing."""
        return ContainerConfig(
            cpu=1000,
            memory=1024,
            max_concurrency=50,
            timeout=300,
            environment_variables={"ENV": "test", "DEBUG": "false"},
        )

    @pytest.fixture
    def serverless_container(self, container_config):
        """Create a ServerlessContainer instance for testing."""
        return ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            region="fr-par",
            tags={"team": "platform"},
        )

    def test_serverless_container_initialization(self, serverless_container, container_config):
        """Test that ServerlessContainer initializes correctly."""
        assert serverless_container.name == "test-container"
        assert serverless_container.environment == "dev"
        assert serverless_container.config == container_config
        assert serverless_container.image_uri == "rg.fr-par.scw.cloud/test-image:latest"
        assert serverless_container.project_id == "test-project-123"
        assert serverless_container.region == "fr-par"
        assert serverless_container.tags == {"team": "platform"}
        assert serverless_container.namespace is None
        assert serverless_container.container is None

    def test_serverless_container_initialization_with_defaults(self):
        """Test ServerlessContainer initialization with minimal parameters."""
        config = ContainerConfig()
        container = ServerlessContainer(
            name="minimal-container",
            environment="staging",
            config=config,
            image_uri="rg.fr-par.scw.cloud/minimal-image:latest",
            project_id="test-project-456",
        )

        assert container.name == "minimal-container"
        assert container.environment == "staging"
        assert container.region == "fr-par"  # Default value
        assert container.tags == {}  # Default empty dict

    def test_serverless_container_invalid_config_validation(self):
        """Test that invalid container configuration raises validation error."""
        with pytest.raises(ValidationError):
            ContainerConfig(cpu=50, memory=1024)  # CPU too low

    @patch("infra.components.serverless_container.scaleway.containers.Namespace")
    @patch("infra.components.serverless_container.scaleway.containers.Container")
    @patch("infra.components.serverless_container.pulumi_helpers.log_resource_creation")
    def test_create_success(self, mock_log, mock_container_class, mock_namespace_class, serverless_container):
        """Test successful creation of serverless container infrastructure."""
        # Mock the namespace and container objects
        mock_namespace = MagicMock()
        mock_container = MagicMock()
        mock_namespace_class.return_value = mock_namespace
        mock_container_class.return_value = mock_container

        # Call create method
        serverless_container.create()

        # Verify logging was called
        mock_log.assert_called_once_with(
            "ServerlessContainer",
            "test-container",
            environment="dev",
            cpu=1000,
            memory=1024,
        )

        # Verify namespace was created
        mock_namespace_class.assert_called_once()
        namespace_args = mock_namespace_class.call_args[1]
        assert namespace_args["name"] == "test-container-ns-dev"
        assert namespace_args["project_id"] == "test-project-123"
        assert namespace_args["region"] == "fr-par"

        # Verify container was created
        mock_container_class.assert_called_once()
        container_args = mock_container_class.call_args[1]
        assert container_args["name"] == "test-container-dev"
        assert container_args["registry_image"] == "rg.fr-par.scw.cloud/test-image:latest"
        assert container_args["cpu_limit"] == 1000
        assert container_args["memory_limit"] == 1024
        assert container_args["max_concurrency"] == 50
        assert container_args["timeout"] == 300
        assert container_args["privacy"] == "public"
        assert container_args["protocol"] == "http1"
        assert container_args["deploy"] is True

        # Verify environment variables
        env_vars = container_args["environment_variables"]
        assert env_vars["ENV"] == "test"
        assert env_vars["DEBUG"] == "false"
        assert env_vars["LOG_LEVEL"] == "info"  # Default added

    @patch("infra.components.serverless_container.scaleway.containers.Namespace")
    @patch("infra.components.serverless_container.scaleway.containers.Container")
    @patch("infra.components.serverless_container.pulumi_helpers.handle_error")
    def test_create_error_handling(
        self, mock_handle_error, mock_container_class, mock_namespace_class, serverless_container
    ):
        """Test error handling during container creation."""
        # Make namespace creation fail
        mock_namespace_class.side_effect = Exception("Test error")

        # Call create method
        serverless_container.create()

        # Verify error was handled
        mock_handle_error.assert_called_once()
        error_call_args = mock_handle_error.call_args[0]
        assert isinstance(error_call_args[0], Exception)
        assert "ServerlessContainer.create(test-container)" in str(error_call_args[1])

    def test_create_namespace(self, serverless_container):
        """Test namespace creation method."""
        with patch(
            "infra.components.serverless_container.scaleway.containers.Namespace"
        ) as mock_namespace_class:
            mock_namespace = MagicMock()
            mock_namespace_class.return_value = mock_namespace

            serverless_container._create_namespace()

            # Verify namespace creation with correct parameters
            mock_namespace_class.assert_called_once()
            call_args = mock_namespace_class.call_args
            assert call_args[0][0] == "test-container-namespace"
            assert call_args[1]["name"] == "test-container-ns-dev"
            assert call_args[1]["project_id"] == "test-project-123"
            assert call_args[1]["region"] == "fr-par"
            assert call_args[1]["description"] == "Container namespace for test-container in dev"
            assert call_args[1]["opts"] == serverless_container.opts

    def test_create_container_without_namespace(self, serverless_container):
        """Test that container creation fails without namespace."""
        with pytest.raises(ValueError, match="Namespace must be created before container"):
            serverless_container._create_container()

    def test_create_container_success(self, serverless_container):
        """Test successful container creation."""
        # Mock namespace
        mock_namespace = MagicMock()
        mock_namespace.id = "test-namespace-id"
        serverless_container.namespace = mock_namespace

        with patch(
            "infra.components.serverless_container.scaleway.containers.Container"
        ) as mock_container_class:
            mock_container = MagicMock()
            mock_container_class.return_value = mock_container

            serverless_container._create_container()

            # Verify container creation with correct parameters
            mock_container_class.assert_called_once()
            call_args = mock_container_class.call_args
            assert call_args[0][0] == "test-container-container"
            assert call_args[1]["namespace_id"] == "test-namespace-id"
            assert call_args[1]["name"] == "test-container-dev"
            assert call_args[1]["registry_image"] == "rg.fr-par.scw.cloud/test-image:latest"
            assert call_args[1]["cpu_limit"] == 1000
            assert call_args[1]["memory_limit"] == 1024
            assert call_args[1]["max_concurrency"] == 50
            assert call_args[1]["timeout"] == 300
            assert isinstance(call_args[1]["environment_variables"], dict)
            assert call_args[1]["privacy"] == "public"
            assert call_args[1]["protocol"] == "http1"
            assert call_args[1]["deploy"] is True
            assert call_args[1]["description"] == "Container for test-container in dev"
            assert call_args[1]["opts"] == serverless_container.opts

    def test_get_outputs_empty(self, serverless_container):
        """Test get_outputs returns empty dict when resources not created."""
        outputs = serverless_container.get_outputs()
        assert outputs == {}

    def test_get_outputs_success(self, serverless_container):
        """Test get_outputs returns correct data when resources created."""
        # Mock namespace and container
        mock_namespace = MagicMock()
        mock_namespace.id = "test-namespace-id"
        mock_container = MagicMock()
        mock_container.id = "test-container-id"
        mock_container.domain_name = "test-container.dev.example.com"

        serverless_container.namespace = mock_namespace
        serverless_container.container = mock_container

        outputs = serverless_container.get_outputs()

        expected = {
            "namespace_id": "test-namespace-id",
            "container_id": "test-container-id",
            "endpoint": "test-container.dev.example.com",
            "image_uri": "rg.fr-par.scw.cloud/test-image:latest",
            "cpu": 1000,
            "memory": 1024,
        }

        assert outputs == expected

    def test_get_endpoint_not_created(self, serverless_container):
        """Test get_endpoint raises error when container not created."""
        with pytest.raises(ValueError, match="Container not created yet"):
            serverless_container.get_endpoint()

    def test_get_endpoint_success(self, serverless_container):
        """Test get_endpoint returns container domain name."""
        mock_container = MagicMock()
        mock_container.domain_name = "test-container.dev.example.com"
        serverless_container.container = mock_container

        endpoint = serverless_container.get_endpoint()
        assert endpoint == "test-container.dev.example.com"

    def test_get_namespace_id_not_created(self, serverless_container):
        """Test get_namespace_id raises error when namespace not created."""
        with pytest.raises(ValueError, match="Namespace not created yet"):
            serverless_container.get_namespace_id()

    def test_get_namespace_id_success(self, serverless_container):
        """Test get_namespace_id returns namespace ID."""
        mock_namespace = MagicMock()
        mock_namespace.id = "test-namespace-id"
        serverless_container.namespace = mock_namespace

        namespace_id = serverless_container.get_namespace_id()
        assert namespace_id == "test-namespace-id"

    def test_get_container_id_not_created(self, serverless_container):
        """Test get_container_id raises error when container not created."""
        with pytest.raises(ValueError, match="Container not created yet"):
            serverless_container.get_container_id()

    def test_get_container_id_success(self, serverless_container):
        """Test get_container_id returns container ID."""
        mock_container = MagicMock()
        mock_container.id = "test-container-id"
        serverless_container.container = mock_container

        container_id = serverless_container.get_container_id()
        assert container_id == "test-container-id"

    def test_environment_variables_default_log_level(self, serverless_container):
        """Test that LOG_LEVEL is set to info when not provided."""
        # Mock namespace
        mock_namespace = MagicMock()
        mock_namespace.id = "test-namespace-id"
        serverless_container.namespace = mock_namespace

        with patch(
            "infra.components.serverless_container.scaleway.containers.Container"
        ) as mock_container_class:
            mock_container = MagicMock()
            mock_container_class.return_value = mock_container

            serverless_container._create_container()

            # Get the environment variables from the call
            container_args = mock_container_class.call_args[1]
            env_vars = container_args["environment_variables"]
            assert env_vars["LOG_LEVEL"] == "info"

    def test_environment_variables_custom_log_level(self, serverless_container):
        """Test that custom LOG_LEVEL is preserved when provided."""
        # Mock namespace
        mock_namespace = MagicMock()
        mock_namespace.id = "test-namespace-id"
        serverless_container.namespace = mock_namespace

        # Add custom LOG_LEVEL to config
        serverless_container.config.environment_variables["LOG_LEVEL"] = "debug"

        with patch(
            "infra.components.serverless_container.scaleway.containers.Container"
        ) as mock_container_class:
            mock_container = MagicMock()
            mock_container_class.return_value = mock_container

            serverless_container._create_container()

            # Get the environment variables from the call
            container_args = mock_container_class.call_args[1]
            env_vars = container_args["environment_variables"]
            assert env_vars["LOG_LEVEL"] == "debug"

    def test_repr(self, serverless_container):
        """Test string representation of ServerlessContainer."""
        expected = "ServerlessContainer(name=test-container, environment=dev)"
        assert repr(serverless_container) == expected


class TestServerlessContainerSecretIntegration:
    """Tests for ServerlessContainer secret integration."""

    @pytest.fixture
    def secret_configs(self):
        """Create secret configurations for testing."""
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
        )

    @pytest.fixture
    def container_config_with_secrets(self):
        """Create a container config with secret environment variables."""
        return ContainerConfig(
            cpu=1000,
            memory=1024,
            environment_variables={"ENV": "test"},
            secret_environment_variables={"DIRECT_SECRET": "direct-value"},
        )

    def test_container_config_with_secret_env_vars(self):
        """Test ContainerConfig accepts secret_environment_variables."""
        config = ContainerConfig(
            cpu=1000,
            memory=1024,
            secret_environment_variables={"SECRET_KEY": "secret-value"},
        )
        assert config.secret_environment_variables == {"SECRET_KEY": "secret-value"}

    def test_container_config_default_secret_env_vars(self):
        """Test ContainerConfig has empty secret_environment_variables by default."""
        config = ContainerConfig()
        assert config.secret_environment_variables == {}

    def test_serverless_container_with_secret_manager(self, container_config_with_secrets, secret_manager):
        """Test ServerlessContainer initialization with SecretManager."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config_with_secrets,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            secret_manager=secret_manager,
            secret_mappings={
                "db-password": "DATABASE_PASSWORD",
                "api-key": "API_KEY",
            },
        )

        assert container.secret_manager == secret_manager
        assert container.secret_mappings == {
            "db-password": "DATABASE_PASSWORD",
            "api-key": "API_KEY",
        }

    def test_build_secret_environment_variables_from_config(self, container_config_with_secrets):
        """Test building secret env vars from ContainerConfig."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config_with_secrets,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
        )

        secret_env_vars = container._build_secret_environment_variables()
        assert secret_env_vars == {"DIRECT_SECRET": "direct-value"}

    def test_build_secret_environment_variables_from_secret_manager(self, secret_manager):
        """Test building secret env vars from SecretManager."""
        config = ContainerConfig(cpu=1000, memory=1024)
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            secret_manager=secret_manager,
            secret_mappings={
                "db-password": "DATABASE_PASSWORD",
                "api-key": "API_KEY",
            },
        )

        secret_env_vars = container._build_secret_environment_variables()
        assert secret_env_vars == {
            "DATABASE_PASSWORD": "super-secret-password",
            "API_KEY": "api-key-12345",
        }

    def test_build_secret_environment_variables_combined(self, container_config_with_secrets, secret_manager):
        """Test building secret env vars from both config and SecretManager."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config_with_secrets,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            secret_manager=secret_manager,
            secret_mappings={"db-password": "DATABASE_PASSWORD"},
        )

        secret_env_vars = container._build_secret_environment_variables()
        assert secret_env_vars == {
            "DIRECT_SECRET": "direct-value",
            "DATABASE_PASSWORD": "super-secret-password",
        }

    def test_build_secret_environment_variables_missing_secret(self, secret_manager):
        """Test building secret env vars with missing secret logs warning."""
        config = ContainerConfig(cpu=1000, memory=1024)
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            secret_manager=secret_manager,
            secret_mappings={"nonexistent-secret": "MISSING_VAR"},
        )

        secret_env_vars = container._build_secret_environment_variables()
        # Missing secret should not be in result
        assert "MISSING_VAR" not in secret_env_vars

    @patch("infra.components.serverless_container.scaleway.containers.Namespace")
    @patch("infra.components.serverless_container.scaleway.containers.Container")
    @patch("infra.components.serverless_container.pulumi_helpers.log_resource_creation")
    def test_create_container_with_secrets(
        self,
        mock_log,
        mock_container_class,
        mock_namespace_class,
        container_config_with_secrets,
        secret_manager,
    ):
        """Test container creation includes secret environment variables."""
        mock_namespace = MagicMock()
        mock_namespace.id = "test-namespace-id"
        mock_namespace_class.return_value = mock_namespace

        mock_container = MagicMock()
        mock_container_class.return_value = mock_container

        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config_with_secrets,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            secret_manager=secret_manager,
            secret_mappings={"db-password": "DATABASE_PASSWORD"},
        )

        container.create()

        # Verify container was created with secret_environment_variables
        mock_container_class.assert_called_once()
        container_args = mock_container_class.call_args[1]
        assert "secret_environment_variables" in container_args
        assert container_args["secret_environment_variables"] == {
            "DIRECT_SECRET": "direct-value",
            "DATABASE_PASSWORD": "super-secret-password",
        }

    @patch("infra.components.serverless_container.scaleway.containers.Namespace")
    @patch("infra.components.serverless_container.scaleway.containers.Container")
    @patch("infra.components.serverless_container.pulumi_helpers.log_resource_creation")
    def test_create_container_without_secrets(
        self,
        mock_log,
        mock_container_class,
        mock_namespace_class,
    ):
        """Test container creation without secrets doesn't include secret_env_vars."""
        mock_namespace = MagicMock()
        mock_namespace.id = "test-namespace-id"
        mock_namespace_class.return_value = mock_namespace

        mock_container = MagicMock()
        mock_container_class.return_value = mock_container

        config = ContainerConfig(cpu=1000, memory=1024)
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
        )

        container.create()

        # Verify container was created without secret_environment_variables
        mock_container_class.assert_called_once()
        container_args = mock_container_class.call_args[1]
        assert "secret_environment_variables" not in container_args


class TestServerlessContainerPrivateNetworkIntegration:
    """Tests for ServerlessContainer private network integration."""

    @pytest.fixture
    def container_config(self):
        """Create a valid container configuration for testing."""
        return ContainerConfig(
            cpu=1000,
            memory=1024,
            environment_variables={"ENV": "test"},
        )

    @pytest.fixture
    def network_config_enabled(self):
        """Create a network configuration with private network enabled."""
        return NetworkConfig(
            enable_private_network=True,
            cidr_block="10.0.0.0/24",
        )

    @pytest.fixture
    def network_config_disabled(self):
        """Create a network configuration with private network disabled."""
        return NetworkConfig(
            enable_private_network=False,
        )

    @pytest.fixture
    def private_network_enabled(self, network_config_enabled):
        """Create a PrivateNetwork instance with private network enabled."""
        return PrivateNetwork(
            name="test-network",
            environment="dev",
            config=network_config_enabled,
            project_id="test-project-123",
            region="fr-par",
        )

    @pytest.fixture
    def private_network_disabled(self, network_config_disabled):
        """Create a PrivateNetwork instance with private network disabled."""
        return PrivateNetwork(
            name="test-network",
            environment="dev",
            config=network_config_disabled,
            project_id="test-project-123",
            region="fr-par",
        )

    def test_serverless_container_with_private_network(self, container_config, private_network_enabled):
        """Test ServerlessContainer initialization with PrivateNetwork."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            private_network=private_network_enabled,
        )

        assert container.private_network == private_network_enabled

    def test_serverless_container_without_private_network(self, container_config):
        """Test ServerlessContainer initialization without PrivateNetwork."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
        )

        assert container.private_network is None

    def test_is_connected_to_private_network_true(self, container_config, private_network_enabled):
        """Test is_connected_to_private_network returns True when connected."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            private_network=private_network_enabled,
        )

        assert container.is_connected_to_private_network() is True

    def test_is_connected_to_private_network_false_no_network(self, container_config):
        """Test is_connected_to_private_network returns False when no network."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
        )

        assert container.is_connected_to_private_network() is False

    def test_is_connected_to_private_network_false_disabled(self, container_config, private_network_disabled):
        """Test is_connected_to_private_network returns False when network disabled."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            private_network=private_network_disabled,
        )

        assert container.is_connected_to_private_network() is False

    def test_get_private_network_id_none_when_no_network(self, container_config):
        """Test _get_private_network_id returns None when no network configured."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
        )

        assert container._get_private_network_id() is None

    def test_get_private_network_id_none_when_disabled(self, container_config, private_network_disabled):
        """Test _get_private_network_id returns None when network disabled."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            private_network=private_network_disabled,
        )

        assert container._get_private_network_id() is None

    def test_get_private_network_id_none_when_not_created(self, container_config, private_network_enabled):
        """Test _get_private_network_id returns None when network not created yet."""
        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            private_network=private_network_enabled,
        )

        # Network is enabled but not created yet, should return None
        assert container._get_private_network_id() is None

    @patch("infra.components.serverless_container.scaleway.containers.Namespace")
    @patch("infra.components.serverless_container.scaleway.containers.Container")
    @patch("infra.components.serverless_container.pulumi_helpers.log_resource_creation")
    def test_create_container_with_private_network(
        self,
        mock_log,
        mock_container_class,
        mock_namespace_class,
        container_config,
        private_network_enabled,
    ):
        """Test container creation includes private_network_id when configured."""
        mock_namespace = MagicMock()
        mock_namespace.id = "test-namespace-id"
        mock_namespace_class.return_value = mock_namespace

        mock_container = MagicMock()
        mock_container_class.return_value = mock_container

        # Mock the private network to return a network ID
        mock_pn = MagicMock()
        mock_pn.id = "test-private-network-id"
        private_network_enabled.private_network = mock_pn

        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            private_network=private_network_enabled,
        )

        container.create()

        # Verify container was created with private_network_id
        mock_container_class.assert_called_once()
        container_args = mock_container_class.call_args[1]
        assert "private_network_id" in container_args
        assert container_args["private_network_id"] == "test-private-network-id"

    @patch("infra.components.serverless_container.scaleway.containers.Namespace")
    @patch("infra.components.serverless_container.scaleway.containers.Container")
    @patch("infra.components.serverless_container.pulumi_helpers.log_resource_creation")
    def test_create_container_without_private_network(
        self,
        mock_log,
        mock_container_class,
        mock_namespace_class,
        container_config,
    ):
        """Test container creation without private_network_id when not configured."""
        mock_namespace = MagicMock()
        mock_namespace.id = "test-namespace-id"
        mock_namespace_class.return_value = mock_namespace

        mock_container = MagicMock()
        mock_container_class.return_value = mock_container

        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
        )

        container.create()

        # Verify container was created without private_network_id
        mock_container_class.assert_called_once()
        container_args = mock_container_class.call_args[1]
        assert "private_network_id" not in container_args

    @patch("infra.components.serverless_container.scaleway.containers.Namespace")
    @patch("infra.components.serverless_container.scaleway.containers.Container")
    @patch("infra.components.serverless_container.pulumi_helpers.log_resource_creation")
    def test_create_container_with_disabled_private_network(
        self,
        mock_log,
        mock_container_class,
        mock_namespace_class,
        container_config,
        private_network_disabled,
    ):
        """Test container creation without private_network_id when network disabled."""
        mock_namespace = MagicMock()
        mock_namespace.id = "test-namespace-id"
        mock_namespace_class.return_value = mock_namespace

        mock_container = MagicMock()
        mock_container_class.return_value = mock_container

        container = ServerlessContainer(
            name="test-container",
            environment="dev",
            config=container_config,
            image_uri="rg.fr-par.scw.cloud/test-image:latest",
            project_id="test-project-123",
            private_network=private_network_disabled,
        )

        container.create()

        # Verify container was created without private_network_id
        mock_container_class.assert_called_once()
        container_args = mock_container_class.call_args[1]
        assert "private_network_id" not in container_args
