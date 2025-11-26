"""Private Network component for Scaleway VPC Private Network."""

import logging
from typing import Any, Optional

import pulumi
import pulumiverse_scaleway as scaleway

from infra.components import BaseComponent
from infra.config.models import NetworkConfig
from infra.utils import pulumi_helpers, scaleway_helpers, validation

logger = logging.getLogger(__name__)


class PrivateNetwork(BaseComponent):
    """
    Private Network component for Scaleway VPC.

    Manages private network creation with IPv4/IPv6 subnet configuration
    for service isolation. Containers and databases can be attached to
    this network for secure inter-service communication.

    Note: Private network integration with Serverless Containers is a beta feature
    and requires VPC integration to be activated on the container namespace.
    """

    def __init__(
        self,
        name: str,
        environment: str,
        config: NetworkConfig,
        project_id: str,
        region: str = "fr-par",
        tags: Optional[dict[str, str]] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """
        Initialize PrivateNetwork component.

        Args:
            name: Component name
            environment: Environment (dev, staging, production)
            config: NetworkConfig with CIDR block and network settings
            project_id: Scaleway project ID
            region: Scaleway region (default: fr-par)
            tags: Optional tags for resources
            opts: Optional Pulumi resource options
        """
        super().__init__(name, environment, tags, opts)
        self.config = config
        self.project_id = project_id
        self.region = region

        # Validate configuration
        if config.enable_private_network:
            validation.validate_cidr_block(config.cidr_block)

        # Initialize resource references
        self.vpc: Optional[scaleway.network.Vpc] = None
        self.private_network: Optional[scaleway.network.PrivateNetwork] = None

    def create(self) -> None:
        """Create the private network infrastructure."""
        if not self.config.enable_private_network:
            logger.info(f"Private network disabled for '{self.name}', skipping creation")
            return

        try:
            pulumi_helpers.log_resource_creation(
                "PrivateNetwork",
                self.name,
                environment=self.environment,
                cidr_block=self.config.cidr_block,
            )

            # Create VPC first (required for private networks)
            self._create_vpc()

            # Create private network with subnet
            self._create_private_network()

            logger.info(f"PrivateNetwork '{self.name}' created successfully")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"PrivateNetwork.create({self.name})")

    def _create_vpc(self) -> None:
        """Create VPC for the private network."""
        vpc_name = scaleway_helpers.format_resource_name(f"{self.name}-vpc", self.environment)

        logger.debug(f"Creating VPC: {vpc_name}")

        self.vpc = scaleway.network.Vpc(
            f"{self.name}-vpc",
            name=vpc_name,
            project_id=self.project_id,
            region=self.region,
            tags=self._format_tags_list(),
            # Enable routing between private networks in the VPC
            enable_routing=True,
            opts=self.opts,
        )

    def _create_private_network(self) -> None:
        """Create private network with IPv4 subnet configuration."""
        if not self.vpc:
            raise ValueError("VPC must be created before private network")

        network_name = scaleway_helpers.format_resource_name(f"{self.name}-pn", self.environment)

        logger.debug(f"Creating private network: {network_name}")

        # Create private network with IPv4 subnet
        pn_opts = pulumi.ResourceOptions(
            parent=self.vpc,
            depends_on=[self.vpc],
        )

        self.private_network = scaleway.network.PrivateNetwork(
            f"{self.name}-private-network",
            name=network_name,
            project_id=self.project_id,
            region=self.region,
            vpc_id=self.vpc.id,
            ipv4_subnet={
                "subnet": self.config.cidr_block,
            },
            tags=self._format_tags_list(),
            opts=pn_opts,
        )

    def _format_tags_list(self) -> list[str]:
        """
        Format tags as a list of strings for Scaleway resources.

        Scaleway VPC resources use a list of strings for tags.

        Returns:
            list[str]: Tags as list of strings
        """
        tags_list = [
            f"environment:{self.environment}",
            f"component:{self.name}",
            "managed-by:pulumi",
        ]

        # Add custom tags
        for key, value in self.tags.items():
            tags_list.append(f"{key}:{value}")

        return tags_list

    def get_outputs(self) -> dict[str, Any]:
        """
        Get component outputs.

        Returns:
            dict: Dictionary containing:
                - vpc_id: VPC ID
                - private_network_id: Private network ID
                - cidr_block: Configured CIDR block
                - region: Region where network is deployed
                - enabled: Whether private network is enabled
        """
        if not self.config.enable_private_network:
            return {
                "enabled": False,
                "vpc_id": None,
                "private_network_id": None,
                "cidr_block": None,
                "region": self.region,
            }

        return {
            "enabled": True,
            "vpc_id": self.vpc.id if self.vpc else None,
            "private_network_id": self.private_network.id if self.private_network else None,
            "cidr_block": self.config.cidr_block,
            "region": self.region,
        }

    def get_vpc_id(self) -> pulumi.Output:
        """
        Get VPC ID.

        Returns:
            pulumi.Output: VPC ID

        Raises:
            ValueError: If VPC not created or private network disabled
        """
        if not self.config.enable_private_network:
            raise ValueError("Private network is disabled")
        if not self.vpc:
            raise ValueError("VPC not created yet")
        return self.vpc.id

    def get_private_network_id(self) -> pulumi.Output:
        """
        Get private network ID.

        Returns:
            pulumi.Output: Private network ID

        Raises:
            ValueError: If private network not created or disabled
        """
        if not self.config.enable_private_network:
            raise ValueError("Private network is disabled")
        if not self.private_network:
            raise ValueError("Private network not created yet")
        return self.private_network.id

    def get_database_private_network_config(self) -> dict[str, pulumi.Output]:
        """
        Get private network configuration for database attachment.

        Returns the format needed for Scaleway Managed Database
        private network endpoint configuration.

        Returns:
            dict: Private network configuration with:
                - pn_id: Private network ID

        Raises:
            ValueError: If private network not created or disabled
        """
        if not self.config.enable_private_network:
            raise ValueError("Private network is disabled")
        if not self.private_network:
            raise ValueError("Private network not created yet")

        return {
            "pn_id": self.private_network.id,
        }

    def get_container_private_network_config(self) -> dict[str, pulumi.Output]:
        """
        Get private network configuration for serverless container attachment.

        Returns the format needed for Scaleway Serverless Container
        private network configuration.

        Note: This is a beta feature and requires the container namespace
        to have VPC integration activated (activate_vpc_integration=true).

        Returns:
            dict: Private network configuration with:
                - private_network_id: Private network ID

        Raises:
            ValueError: If private network not created or disabled
        """
        if not self.config.enable_private_network:
            raise ValueError("Private network is disabled")
        if not self.private_network:
            raise ValueError("Private network not created yet")

        return {
            "private_network_id": self.private_network.id,
        }

    def is_enabled(self) -> bool:
        """
        Check if private network is enabled.

        Returns:
            bool: True if private network is enabled
        """
        return self.config.enable_private_network
