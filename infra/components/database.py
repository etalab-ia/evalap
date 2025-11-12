"""Database Instance component for Scaleway Managed PostgreSQL."""

import logging
from typing import Any, Optional

import pulumi
import pulumi_scaleway as scaleway

from infra.components import BaseComponent
from infra.config.models import DatabaseConfig
from infra.utils import pulumi_helpers, scaleway_helpers, validation

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
        """
        super().__init__(name, environment, tags, opts)
        self.config = config
        self.project_id = project_id
        self.region = region

        # Validate configuration
        validation.validate_database_config(config.volume_size, config.backup_retention_days)
        validation.validate_database_name(config.database_name)

        # Initialize resource references
        self.instance: Optional[scaleway.DatabaseInstance] = None
        self.database: Optional[scaleway.Database] = None
        self.user: Optional[scaleway.DatabaseUser] = None

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

            # Create user
            self._create_user()

            logger.info(f"DatabaseInstance '{self.name}' created successfully")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"DatabaseInstance.create({self.name})")

    def _create_instance(self) -> None:
        """Create RDB instance with backup configuration."""
        instance_name = scaleway_helpers.format_resource_name(f"{self.name}-db", self.environment)

        logger.debug(f"Creating RDB instance: {instance_name}")

        self.instance = scaleway.DatabaseInstance(
            f"{self.name}-instance",
            name=instance_name,
            engine=self.config.engine,
            node_type="DB-DEV-S",  # Development instance type
            is_ha_cluster=self.config.enable_high_availability,
            project_id=self.project_id,
            region=self.region,
            tags=scaleway_helpers.create_resource_tags(
                self.environment, "database", additional_tags=self.tags
            ),
            opts=self.opts,
        )

    def _create_database(self) -> None:
        """Create default database."""
        if not self.instance:
            raise ValueError("Instance must be created before database")

        logger.debug(f"Creating database: {self.config.database_name}")

        self.database = scaleway.Database(
            f"{self.name}-database",
            instance_id=self.instance.id,
            name=self.config.database_name,
            opts=self.opts,
        )

    def _create_user(self) -> None:
        """Create database user."""
        if not self.instance:
            raise ValueError("Instance must be created before user")

        logger.debug(f"Creating database user: {self.config.user_name}")

        self.user = scaleway.DatabaseUser(
            f"{self.name}-user",
            instance_id=self.instance.id,
            name=self.config.user_name,
            password=pulumi.Config().require_secret("db_password"),
            is_admin=True,
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
            "endpoint": pulumi.Output.concat(self.instance.endpoint_ip, ":", self.instance.endpoint_port),
            "host": self.instance.endpoint_ip,
            "port": self.instance.endpoint_port,
            "database_name": self.config.database_name,
            "username": self.config.user_name,
            "engine": self.config.engine,
            "volume_size_gb": self.config.volume_size,
            "backup_retention_days": self.config.backup_retention_days,
        }

    def get_connection_string(self) -> pulumi.Output:
        """
        Get PostgreSQL connection string.

        Returns:
            pulumi.Output: Connection string (without password)
        """
        if not self.instance:
            raise ValueError("Instance not created yet")

        return pulumi.Output.concat(
            "postgresql://",
            self.config.user_name,
            "@",
            self.instance.endpoint_ip,
            ":",
            self.instance.endpoint_port,
            "/",
            self.config.database_name,
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

    def get_host(self) -> pulumi.Output:
        """
        Get database host.

        Returns:
            pulumi.Output: Database host
        """
        if not self.instance:
            raise ValueError("Instance not created yet")
        return self.instance.endpoint_ip

    def get_port(self) -> pulumi.Output:
        """
        Get database port.

        Returns:
            pulumi.Output: Database port
        """
        if not self.instance:
            raise ValueError("Instance not created yet")
        return self.instance.endpoint_port
