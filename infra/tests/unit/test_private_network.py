"""Unit tests for PrivateNetwork component."""

from unittest.mock import MagicMock, patch

import pytest

from infra.components.private_network import PrivateNetwork
from infra.config.models import NetworkConfig


class TestNetworkConfig:
    """Tests for NetworkConfig model."""

    def test_network_config_defaults(self):
        """Test NetworkConfig with default values."""
        config = NetworkConfig()
        assert config.enable_private_network is False
        assert config.cidr_block == "10.0.0.0/16"
        assert config.enable_nat_gateway is False

    def test_network_config_enabled(self):
        """Test NetworkConfig with private network enabled."""
        config = NetworkConfig(
            enable_private_network=True,
            cidr_block="192.168.0.0/24",
        )
        assert config.enable_private_network is True
        assert config.cidr_block == "192.168.0.0/24"

    def test_network_config_custom_cidr(self):
        """Test NetworkConfig with custom CIDR block."""
        config = NetworkConfig(
            enable_private_network=True,
            cidr_block="172.16.0.0/12",
        )
        assert config.cidr_block == "172.16.0.0/12"


class TestPrivateNetwork:
    """Tests for PrivateNetwork component."""

    @pytest.fixture
    def network_config_enabled(self):
        """Create enabled network configuration for testing."""
        return NetworkConfig(
            enable_private_network=True,
            cidr_block="10.0.0.0/16",
        )

    @pytest.fixture
    def network_config_disabled(self):
        """Create disabled network configuration for testing."""
        return NetworkConfig(
            enable_private_network=False,
        )

    @pytest.fixture
    def private_network(self, network_config_enabled):
        """Create a PrivateNetwork instance for testing."""
        return PrivateNetwork(
            name="test-network",
            environment="dev",
            config=network_config_enabled,
            project_id="test-project-123",
            region="fr-par",
            tags={"team": "platform"},
        )

    @pytest.fixture
    def private_network_disabled(self, network_config_disabled):
        """Create a disabled PrivateNetwork instance for testing."""
        return PrivateNetwork(
            name="test-network",
            environment="dev",
            config=network_config_disabled,
            project_id="test-project-123",
            region="fr-par",
        )

    def test_private_network_initialization(self, private_network, network_config_enabled):
        """Test that PrivateNetwork initializes correctly."""
        assert private_network.name == "test-network"
        assert private_network.environment == "dev"
        assert private_network.config == network_config_enabled
        assert private_network.project_id == "test-project-123"
        assert private_network.region == "fr-par"
        assert private_network.tags == {"team": "platform"}
        assert private_network.vpc is None
        assert private_network.private_network is None

    def test_private_network_initialization_with_defaults(self):
        """Test PrivateNetwork initialization with minimal parameters."""
        config = NetworkConfig(enable_private_network=True)
        pn = PrivateNetwork(
            name="minimal-network",
            environment="staging",
            config=config,
            project_id="test-project-456",
        )

        assert pn.name == "minimal-network"
        assert pn.environment == "staging"
        assert pn.region == "fr-par"  # Default value
        assert pn.tags == {}  # Default empty dict

    def test_format_tags_list(self, private_network):
        """Test that tags are formatted correctly as a list."""
        tags_list = private_network._format_tags_list()

        assert "environment:dev" in tags_list
        assert "component:test-network" in tags_list
        assert "managed-by:pulumi" in tags_list
        assert "team:platform" in tags_list

    @patch("infra.components.private_network.pulumi.ResourceOptions")
    @patch("infra.components.private_network.scaleway.network.Vpc")
    @patch("infra.components.private_network.scaleway.network.PrivateNetwork")
    @patch("infra.components.private_network.pulumi_helpers.log_resource_creation")
    def test_create_success(
        self,
        mock_log,
        mock_pn_class,
        mock_vpc_class,
        mock_resource_opts,
        private_network,
    ):
        """Test successful creation of private network."""
        # Mock the VPC and PrivateNetwork objects
        mock_vpc = MagicMock()
        mock_vpc.id = "vpc-id-123"
        mock_vpc_class.return_value = mock_vpc

        mock_pn = MagicMock()
        mock_pn.id = "pn-id-456"
        mock_pn_class.return_value = mock_pn

        # Call create
        private_network.create()

        # Verify log was called
        mock_log.assert_called_once()

        # Verify VPC was created
        mock_vpc_class.assert_called_once()

        # Verify private network was created
        mock_pn_class.assert_called_once()

        # Verify resources are tracked
        assert private_network.vpc == mock_vpc
        assert private_network.private_network == mock_pn

    @patch("infra.components.private_network.scaleway.network.Vpc")
    @patch("infra.components.private_network.scaleway.network.PrivateNetwork")
    @patch("infra.components.private_network.pulumi_helpers.log_resource_creation")
    def test_create_disabled_skips_creation(
        self,
        mock_log,
        mock_pn_class,
        mock_vpc_class,
        private_network_disabled,
    ):
        """Test that create skips resource creation when disabled."""
        private_network_disabled.create()

        # Verify no resources were created
        mock_vpc_class.assert_not_called()
        mock_pn_class.assert_not_called()
        mock_log.assert_not_called()

        # Verify resources remain None
        assert private_network_disabled.vpc is None
        assert private_network_disabled.private_network is None

    @patch("infra.components.private_network.pulumi.ResourceOptions")
    @patch("infra.components.private_network.scaleway.network.Vpc")
    @patch("infra.components.private_network.scaleway.network.PrivateNetwork")
    @patch("infra.components.private_network.pulumi_helpers.log_resource_creation")
    def test_get_outputs_enabled(
        self,
        mock_log,
        mock_pn_class,
        mock_vpc_class,
        mock_resource_opts,
        private_network,
    ):
        """Test get_outputs returns correct structure when enabled."""
        mock_vpc = MagicMock()
        mock_vpc.id = "vpc-id-123"
        mock_vpc_class.return_value = mock_vpc

        mock_pn = MagicMock()
        mock_pn.id = "pn-id-456"
        mock_pn_class.return_value = mock_pn

        private_network.create()
        outputs = private_network.get_outputs()

        assert outputs["enabled"] is True
        assert outputs["vpc_id"] == "vpc-id-123"
        assert outputs["private_network_id"] == "pn-id-456"
        assert outputs["cidr_block"] == "10.0.0.0/16"
        assert outputs["region"] == "fr-par"

    def test_get_outputs_disabled(self, private_network_disabled):
        """Test get_outputs returns correct structure when disabled."""
        outputs = private_network_disabled.get_outputs()

        assert outputs["enabled"] is False
        assert outputs["vpc_id"] is None
        assert outputs["private_network_id"] is None
        assert outputs["cidr_block"] is None
        assert outputs["region"] == "fr-par"

    @patch("infra.components.private_network.pulumi.ResourceOptions")
    @patch("infra.components.private_network.scaleway.network.Vpc")
    @patch("infra.components.private_network.scaleway.network.PrivateNetwork")
    @patch("infra.components.private_network.pulumi_helpers.log_resource_creation")
    def test_get_vpc_id(
        self,
        mock_log,
        mock_pn_class,
        mock_vpc_class,
        mock_resource_opts,
        private_network,
    ):
        """Test get_vpc_id returns correct ID."""
        mock_vpc = MagicMock()
        mock_vpc.id = "vpc-id-123"
        mock_vpc_class.return_value = mock_vpc

        mock_pn = MagicMock()
        mock_pn_class.return_value = mock_pn

        private_network.create()

        vpc_id = private_network.get_vpc_id()
        assert vpc_id == "vpc-id-123"

    @patch("infra.components.private_network.pulumi.ResourceOptions")
    @patch("infra.components.private_network.scaleway.network.Vpc")
    @patch("infra.components.private_network.scaleway.network.PrivateNetwork")
    @patch("infra.components.private_network.pulumi_helpers.log_resource_creation")
    def test_get_private_network_id(
        self,
        mock_log,
        mock_pn_class,
        mock_vpc_class,
        mock_resource_opts,
        private_network,
    ):
        """Test get_private_network_id returns correct ID."""
        mock_vpc = MagicMock()
        mock_vpc.id = "vpc-id-123"
        mock_vpc_class.return_value = mock_vpc

        mock_pn = MagicMock()
        mock_pn.id = "pn-id-456"
        mock_pn_class.return_value = mock_pn

        private_network.create()

        pn_id = private_network.get_private_network_id()
        assert pn_id == "pn-id-456"

    def test_get_vpc_id_disabled_raises_error(self, private_network_disabled):
        """Test get_vpc_id raises ValueError when disabled."""
        with pytest.raises(ValueError) as exc_info:
            private_network_disabled.get_vpc_id()
        assert "disabled" in str(exc_info.value)

    def test_get_private_network_id_disabled_raises_error(self, private_network_disabled):
        """Test get_private_network_id raises ValueError when disabled."""
        with pytest.raises(ValueError) as exc_info:
            private_network_disabled.get_private_network_id()
        assert "disabled" in str(exc_info.value)

    def test_get_vpc_id_not_created_raises_error(self, private_network):
        """Test get_vpc_id raises ValueError when not created."""
        with pytest.raises(ValueError) as exc_info:
            private_network.get_vpc_id()
        assert "not created" in str(exc_info.value)

    def test_get_private_network_id_not_created_raises_error(self, private_network):
        """Test get_private_network_id raises ValueError when not created."""
        with pytest.raises(ValueError) as exc_info:
            private_network.get_private_network_id()
        assert "not created" in str(exc_info.value)

    @patch("infra.components.private_network.pulumi.ResourceOptions")
    @patch("infra.components.private_network.scaleway.network.Vpc")
    @patch("infra.components.private_network.scaleway.network.PrivateNetwork")
    @patch("infra.components.private_network.pulumi_helpers.log_resource_creation")
    def test_get_database_private_network_config(
        self,
        mock_log,
        mock_pn_class,
        mock_vpc_class,
        mock_resource_opts,
        private_network,
    ):
        """Test get_database_private_network_config returns correct format."""
        mock_vpc = MagicMock()
        mock_vpc_class.return_value = mock_vpc

        mock_pn = MagicMock()
        mock_pn.id = "pn-id-456"
        mock_pn_class.return_value = mock_pn

        private_network.create()

        db_config = private_network.get_database_private_network_config()

        assert "pn_id" in db_config
        assert db_config["pn_id"] == "pn-id-456"

    @patch("infra.components.private_network.pulumi.ResourceOptions")
    @patch("infra.components.private_network.scaleway.network.Vpc")
    @patch("infra.components.private_network.scaleway.network.PrivateNetwork")
    @patch("infra.components.private_network.pulumi_helpers.log_resource_creation")
    def test_get_container_private_network_config(
        self,
        mock_log,
        mock_pn_class,
        mock_vpc_class,
        mock_resource_opts,
        private_network,
    ):
        """Test get_container_private_network_config returns correct format."""
        mock_vpc = MagicMock()
        mock_vpc_class.return_value = mock_vpc

        mock_pn = MagicMock()
        mock_pn.id = "pn-id-456"
        mock_pn_class.return_value = mock_pn

        private_network.create()

        container_config = private_network.get_container_private_network_config()

        assert "private_network_id" in container_config
        assert container_config["private_network_id"] == "pn-id-456"

    def test_get_database_private_network_config_disabled_raises_error(self, private_network_disabled):
        """Test get_database_private_network_config raises ValueError when disabled."""
        with pytest.raises(ValueError) as exc_info:
            private_network_disabled.get_database_private_network_config()
        assert "disabled" in str(exc_info.value)

    def test_get_container_private_network_config_disabled_raises_error(self, private_network_disabled):
        """Test get_container_private_network_config raises ValueError when disabled."""
        with pytest.raises(ValueError) as exc_info:
            private_network_disabled.get_container_private_network_config()
        assert "disabled" in str(exc_info.value)

    def test_is_enabled_true(self, private_network):
        """Test is_enabled returns True when enabled."""
        assert private_network.is_enabled() is True

    def test_is_enabled_false(self, private_network_disabled):
        """Test is_enabled returns False when disabled."""
        assert private_network_disabled.is_enabled() is False


class TestCIDRValidation:
    """Tests for CIDR validation utilities."""

    def test_validate_cidr_block_valid(self):
        """Test valid CIDR blocks pass validation."""
        from infra.utils.validation import validate_cidr_block

        assert validate_cidr_block("10.0.0.0/16") is True
        assert validate_cidr_block("192.168.1.0/24") is True
        assert validate_cidr_block("172.16.0.0/12") is True
        assert validate_cidr_block("0.0.0.0/0") is True

    def test_validate_cidr_block_invalid_format(self):
        """Test invalid CIDR format raises ValueError."""
        from infra.utils.validation import validate_cidr_block

        with pytest.raises(ValueError):
            validate_cidr_block("10.0.0.0")  # missing prefix

        with pytest.raises(ValueError):
            validate_cidr_block("10.0.0/16")  # missing octet

        with pytest.raises(ValueError):
            validate_cidr_block("invalid")  # not a CIDR

    def test_validate_cidr_block_invalid_octet(self):
        """Test invalid IP octet raises ValueError."""
        from infra.utils.validation import validate_cidr_block

        with pytest.raises(ValueError):
            validate_cidr_block("256.0.0.0/16")  # octet > 255

    def test_validate_cidr_block_invalid_prefix(self):
        """Test invalid prefix length raises ValueError."""
        from infra.utils.validation import validate_cidr_block

        with pytest.raises(ValueError):
            validate_cidr_block("10.0.0.0/33")  # prefix > 32

    def test_validate_private_network_cidr_valid(self):
        """Test valid private network CIDRs pass validation."""
        from infra.utils.validation import validate_private_network_cidr

        # 10.0.0.0/8 range
        assert validate_private_network_cidr("10.0.0.0/8") is True
        assert validate_private_network_cidr("10.0.0.0/16") is True
        assert validate_private_network_cidr("10.255.255.0/24") is True

        # 172.16.0.0/12 range
        assert validate_private_network_cidr("172.16.0.0/12") is True
        assert validate_private_network_cidr("172.31.0.0/16") is True

        # 192.168.0.0/16 range
        assert validate_private_network_cidr("192.168.0.0/16") is True
        assert validate_private_network_cidr("192.168.1.0/24") is True

    def test_validate_private_network_cidr_invalid(self):
        """Test non-private CIDRs raise ValueError."""
        from infra.utils.validation import validate_private_network_cidr

        with pytest.raises(ValueError) as exc_info:
            validate_private_network_cidr("8.8.8.0/24")  # public IP
        assert "not a valid private network range" in str(exc_info.value)

        with pytest.raises(ValueError):
            validate_private_network_cidr("172.15.0.0/16")  # outside 172.16-31 range

        with pytest.raises(ValueError):
            validate_private_network_cidr("172.32.0.0/16")  # outside 172.16-31 range

        with pytest.raises(ValueError):
            validate_private_network_cidr("192.169.0.0/16")  # not 192.168.x.x

    def test_validate_network_config_enabled_valid(self):
        """Test valid network config passes validation."""
        from infra.utils.validation import validate_network_config

        config = NetworkConfig(
            enable_private_network=True,
            cidr_block="10.0.0.0/16",
        )
        assert validate_network_config(config) is True

    def test_validate_network_config_disabled_skips_cidr(self):
        """Test disabled network config skips CIDR validation."""
        from infra.utils.validation import validate_network_config

        config = NetworkConfig(
            enable_private_network=False,
            cidr_block="invalid-cidr",  # Would fail if validated
        )
        # Should not raise because private network is disabled
        assert validate_network_config(config) is True
