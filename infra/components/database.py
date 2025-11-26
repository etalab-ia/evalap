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
        """
        super().__init__(name, environment, tags, opts)
        self.config = config
        self.project_id = project_id
        self.region = region
        self.secret_manager = secret_manager
        self.password_secret_name = password_secret_name

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
        """Create RDB instance with backup configuration."""
        instance_name = scaleway_helpers.format_resource_name(f"{self.name}-db", self.environment)

        logger.debug(f"Creating RDB instance: {instance_name}")

        # Get password from secret manager or Pulumi config
        password = self._get_password()

        self.instance = scaleway.databases.Instance(
            f"{self.name}-instance",
            name=instance_name,
            engine=self.config.engine,
            node_type="DB-DEV-S",  # Development instance type
            is_ha_cluster=self.config.enable_high_availability,
            user_name=self.config.user_name,
            password=password,
            project_id=self.project_id,
            region=self.region,
            opts=self.opts,
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
                - endpoint: Database endpoint (host:port)
                - host: Database host
                - port: Database port
                - database_name: Database name
                - username: Database username
                - engine: Database engine
        """
        if not self.instance:
            return {}

        return {
            "instance_id": self.instance.id,
            "endpoint_ip": self.instance.endpoint_ip,
            "endpoint_port": self.instance.endpoint_port,
            "database_name": self.config.database_name,
            "username": self.config.user_name,
            "engine": self.config.engine,
            "volume_size_gb": self.config.volume_size,
            "backup_retention_days": self.config.backup_retention_days,
        }

    def get_connection_string(self) -> pulumi.Output[str]:
        """
        Get PostgreSQL connection string.

        Returns:
            pulumi.Output[str]: Connection string (without password)

        Note:
            endpoint_ip and endpoint_port are deprecated but still functional.
            The recommended approach is to use load_balancer or private_network attributes.
        """
        if not self.instance:
            raise ValueError("Instance not created yet")

        # Use deprecated but functional endpoint_ip and endpoint_port
        # These are still available as output properties
        return pulumi.Output.all(
            self.instance.endpoint_ip,
            self.instance.endpoint_port,
        ).apply(
            lambda args: f"postgresql://{self.config.user_name}@{args[0]}:{args[1]}/{self.config.database_name}"
        )

    def get_instance_id(self) -> pulumi.Output:
        """
        Get RDB instance ID.

        Returns:
            pulumi.Output: Instance ID
        """
        if not self.instance:
            raise ValueError("Instance not created yet")
        return self.instance.id
