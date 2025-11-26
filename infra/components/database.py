"""Database Instance component for Scaleway Managed PostgreSQL."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional, Union

import pulumi
import pulumiverse_scaleway as scaleway

from infra.components import BaseComponent
from infra.config.models import DatabaseConfig
from infra.utils import pulumi_helpers, scaleway_helpers, validation

if TYPE_CHECKING:
    from infra.components.private_network import PrivateNetwork
    from infra.components.secret_manager import SecretManager

logger = logging.getLogger(__name__)


class DatabaseInstance(BaseComponent):
    """
    Managed PostgreSQL Database Instance component.

    Manages database provisioning, backup configuration, and connection details.
    """

    def __init__(
        self,
        name: str,
        environment: str,
        config: DatabaseConfig,
        project_id: str,
        region: str = "fr-par",
        tags: Optional[dict[str, str]] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
        secret_manager: Optional[SecretManager] = None,
        password_secret_name: Optional[str] = None,
        private_network: Optional[PrivateNetwork] = None,
        private_network_ip: Optional[str] = None,
    ):
        """
        Initialize DatabaseInstance component.

        Args:
            name: Component name
            environment: Environment (dev, staging, production)
            config: DatabaseConfig with volume size, backup settings, etc.
            project_id: Scaleway project ID
            region: Scaleway region (default: fr-par)
            tags: Optional tags for resources
            opts: Optional Pulumi resource options
            secret_manager: Optional SecretManager instance for credential management.
                When provided, the database password will be retrieved from the secret
                manager instead of Pulumi config.
            password_secret_name: Name of the secret containing the database password.
                Required when secret_manager is provided.
            private_network: Optional PrivateNetwork instance for network isolation.
                When provided, the database will be attached to the private network
                and accessible only from within the VPC.
            private_network_ip: Static IP address within the private network CIDR.
                If not provided, IPAM will automatically assign an IP address.
                Format: "x.x.x.x/mask" (e.g., "172.16.20.4/22")
        """
        super().__init__(name, environment, tags, opts)
        self.config = config
        self.project_id = project_id
        self.region = region
        self.secret_manager = secret_manager
        self.password_secret_name = password_secret_name
        self.private_network = private_network
        self.private_network_ip = private_network_ip

        # Validate secret manager configuration
        if secret_manager is not None and password_secret_name is None:
            raise ValueError("password_secret_name is required when secret_manager is provided")
        if password_secret_name is not None and secret_manager is None:
            raise ValueError("secret_manager is required when password_secret_name is provided")

        # Validate configuration
        validation.validate_database_config(config.volume_size, config.backup_retention_days)
        validation.validate_database_name(config.database_name)

        # Initialize resource references
        self.instance: Optional[scaleway.databases.Instance] = None
        self.database: Optional[scaleway.databases.Database] = None
        self.user: Optional[scaleway.databases.User] = None

    def create(self) -> None:
        """Create the managed database infrastructure."""
        try:
            pulumi_helpers.log_resource_creation(
                "DatabaseInstance",
                self.name,
                environment=self.environment,
                engine=self.config.engine,
                volume_size=self.config.volume_size,
                backup_retention=self.config.backup_retention_days,
            )

            # Create RDB instance
            self._create_instance()

            # Create database
            self._create_database()

            logger.info(f"DatabaseInstance '{self.name}' created successfully")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"DatabaseInstance.create({self.name})")

    def _create_instance(self) -> None:
        """Create RDB instance with backup configuration and optional private network."""
        instance_name = scaleway_helpers.format_resource_name(f"{self.name}-db", self.environment)

        logger.debug(f"Creating RDB instance: {instance_name}")

        # Get password from secret manager or Pulumi config
        password = self._get_password()

        # Build private network configuration if provided
        private_network_config = self._build_private_network_config()

        self.instance = scaleway.databases.Instance(
            f"{self.name}-instance",
            name=instance_name,
            engine=self.config.engine,
            node_type="DB-DEV-S",  # Development instance type
            is_ha_cluster=self.config.enable_high_availability,
            encryption_at_rest=self.config.enable_encryption_at_rest,
            user_name=self.config.user_name,
            password=password,
            project_id=self.project_id,
            region=self.region,
            private_network=private_network_config,
            # Enable public endpoint via load_balancer (replaces deprecated endpoint_ip/endpoint_port)
            load_balancer=scaleway.databases.InstanceLoadBalancerArgs(),
            opts=self.opts,
        )

    def _build_private_network_config(
        self,
    ) -> Optional[scaleway.databases.InstancePrivateNetworkArgs]:
        """
        Build private network configuration for the database instance.

        Returns:
            InstancePrivateNetworkArgs if private network is configured, None otherwise.

        The configuration supports two modes:
        1. Static IP: When private_network_ip is provided, uses the specified IP address
        2. IPAM: When private_network_ip is None, enables automatic IP assignment via IPAM
        """
        if self.private_network is None:
            return None

        if not self.private_network.is_enabled():
            logger.warning(
                f"Private network '{self.private_network.name}' is disabled, "
                "skipping database private network configuration"
            )
            return None

        pn_id = self.private_network.get_private_network_id()

        if self.private_network_ip:
            # Static IP mode: use the provided IP address
            logger.debug(f"Configuring database with static private network IP: {self.private_network_ip}")
            return scaleway.databases.InstancePrivateNetworkArgs(
                pn_id=pn_id,
                ip_net=self.private_network_ip,
            )
        else:
            # IPAM mode: let Scaleway automatically assign an IP
            logger.debug("Configuring database with IPAM-managed private network IP")
            return scaleway.databases.InstancePrivateNetworkArgs(
                pn_id=pn_id,
                enable_ipam=True,
            )

    def _get_password(self) -> Union[str, pulumi.Output[str]]:
        """
        Get database password from secret manager or Pulumi config.

        Returns:
            Password string or Pulumi Output containing the password.

        Priority:
            1. Secret Manager (if configured)
            2. Pulumi Config (fallback)
        """
        if self.secret_manager is not None and self.password_secret_name is not None:
            logger.debug(f"Using password from SecretManager secret: {self.password_secret_name}")
            return self.secret_manager.get_secret_data(self.password_secret_name)

        logger.debug("Using password from Pulumi config")
        return pulumi.Config().require_secret("db_password")

    def _create_database(self) -> None:
        """Create default database."""
        if not self.instance:
            raise ValueError("Instance must be created before database")

        logger.debug(f"Creating database: {self.config.database_name}")

        self.database = scaleway.databases.Database(
            f"{self.name}-database",
            instance_id=self.instance.id,
            name=self.config.database_name,
            opts=self.opts,
        )

    def get_outputs(self) -> dict[str, Any]:
        """
        Get component outputs.

        Returns:
            dict: Dictionary containing:
                - instance_id: RDB instance ID
                - endpoint_ip: Database public endpoint IP (via load_balancer)
                - endpoint_port: Database public endpoint port (via load_balancer)
                - database_name: Database name
                - username: Database username
                - engine: Database engine
                - volume_size_gb: Volume size in GB
                - backup_retention_days: Backup retention in days
                - private_network_enabled: Whether private network is configured
                - private_network_endpoint: Private network endpoint info (if configured)
        """
        if not self.instance:
            return {}

        outputs = {
            "instance_id": self.instance.id,
            "endpoint_ip": self.instance.load_balancer.ip,
            "endpoint_port": self.instance.load_balancer.port,
            "database_name": self.config.database_name,
            "username": self.config.user_name,
            "engine": self.config.engine,
            "volume_size_gb": self.config.volume_size,
            "backup_retention_days": self.config.backup_retention_days,
            "encryption_at_rest_enabled": self.config.enable_encryption_at_rest,
            "private_network_enabled": self.private_network is not None and self.private_network.is_enabled(),
        }

        # Add private network endpoint info if configured
        if self.private_network is not None and self.private_network.is_enabled():
            outputs["private_network_endpoint"] = {
                "hostname": self.instance.private_network.hostname,
                "ip": self.instance.private_network.ip,
                "port": self.instance.private_network.port,
                "pn_id": self.instance.private_network.pn_id,
            }

        return outputs

    def get_connection_string(self, use_private_network: bool = False) -> pulumi.Output[str]:
        """
        Get PostgreSQL connection string.

        Args:
            use_private_network: If True and private network is configured,
                returns connection string using private network endpoint.
                If False, returns public endpoint connection string.

        Returns:
            pulumi.Output[str]: Connection string (without password)
        """
        if not self.instance:
            raise ValueError("Instance not created yet")

        if use_private_network:
            return self.get_private_network_connection_string()

        # Use load_balancer endpoint (replaces deprecated endpoint_ip/endpoint_port)
        return pulumi.Output.all(
            self.instance.load_balancer.ip,
            self.instance.load_balancer.port,
        ).apply(
            lambda args: f"postgresql://{self.config.user_name}@{args[0]}:{args[1]}/{self.config.database_name}"
        )

    def get_private_network_connection_string(self) -> pulumi.Output[str]:
        """
        Get PostgreSQL connection string using private network endpoint.

        Returns:
            pulumi.Output[str]: Connection string using private network (without password)

        Raises:
            ValueError: If instance not created or private network not configured

        Note:
            This connection string should only be used from services within
            the same private network (e.g., serverless containers attached
            to the same VPC).
        """
        if not self.instance:
            raise ValueError("Instance not created yet")

        if self.private_network is None or not self.private_network.is_enabled():
            raise ValueError(
                "Private network not configured. Use get_connection_string() "
                "for public endpoint or configure private_network parameter."
            )

        # Use private network endpoint (hostname/ip and port)
        return pulumi.Output.all(
            self.instance.private_network.hostname,
            self.instance.private_network.port,
        ).apply(
            lambda args: f"postgresql://{self.config.user_name}@{args[0]}:{args[1]}/{self.config.database_name}"
        )

    def get_private_network_host(self) -> pulumi.Output[str]:
        """
        Get database hostname on private network.

        Returns:
            pulumi.Output[str]: Private network hostname

        Raises:
            ValueError: If instance not created or private network not configured
        """
        if not self.instance:
            raise ValueError("Instance not created yet")

        if self.private_network is None or not self.private_network.is_enabled():
            raise ValueError("Private network not configured")

        return self.instance.private_network.hostname

    def get_private_network_port(self) -> pulumi.Output[int]:
        """
        Get database port on private network.

        Returns:
            pulumi.Output[int]: Private network port

        Raises:
            ValueError: If instance not created or private network not configured
        """
        if not self.instance:
            raise ValueError("Instance not created yet")

        if self.private_network is None or not self.private_network.is_enabled():
            raise ValueError("Private network not configured")

        return self.instance.private_network.port

    def is_private_network_enabled(self) -> bool:
        """
        Check if private network is configured for this database.

        Returns:
            bool: True if private network is configured and enabled
        """
        return self.private_network is not None and self.private_network.is_enabled()

    def get_instance_id(self) -> pulumi.Output:
        """
        Get RDB instance ID.

        Returns:
            pulumi.Output: Instance ID
        """
        if not self.instance:
            raise ValueError("Instance not created yet")
        return self.instance.id
