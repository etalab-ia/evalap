"""Development stack implementation combining all infrastructure components."""

import logging
from typing import Optional

import pulumi

from infra.components.database import DatabaseInstance
from infra.components.object_storage import ObjectStorageBucket
from infra.components.serverless_container import ServerlessContainer
from infra.config.models import StackConfiguration
from infra.utils import pulumi_helpers

logger = logging.getLogger(__name__)


class DevelopmentStack:
    """Development stack combining ServerlessContainer, DatabaseInstance, and ObjectStorageBucket."""

    def __init__(self, config: StackConfiguration):
        """
        Initialize development stack.

        Args:
            config: StackConfiguration with all component configurations
        """
        self.config = config
        self.stack_name = pulumi.get_stack()

        # Initialize component references
        self.container: Optional[ServerlessContainer] = None
        self.database: Optional[DatabaseInstance] = None
        self.storage: Optional[ObjectStorageBucket] = None

        logger.info(f"Initializing development stack: {self.stack_name}")

    def create(self) -> None:
        """Create all infrastructure components for the development stack."""
        try:
            logger.info(f"Creating development stack: {self.stack_name}")

            # Create database first (other components may depend on it)
            self._create_database()

            # Create container
            self._create_container()

            # Create object storage
            self._create_storage()

            # Export all outputs
            self._export_outputs()

            logger.info(f"Development stack '{self.stack_name}' created successfully")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"DevelopmentStack.create({self.stack_name})")

    def _create_database(self) -> None:
        """Create managed PostgreSQL database instance."""
        logger.debug("Creating database component")

        self.database = DatabaseInstance(
            name="evalap-db",
            environment=self.config.environment,
            config=self.config.database,
            project_id=self.config.project_id,
            region=self.config.region,
            tags=self.config.tags,
        )

        self.database.create()

    def _create_container(self) -> None:
        """Create serverless container."""
        logger.debug("Creating container component")

        # Use a public hello-world HTTP server image - should be provided via config or environment
        # Using testcontainers/helloworld which listens on port 8080
        image_uri = pulumi.Config().get("container_image_uri") or "docker.io/testcontainers/helloworld:latest"

        self.container = ServerlessContainer(
            name="evalap-api",
            environment=self.config.environment,
            config=self.config.container,
            image_uri=image_uri,
            project_id=self.config.project_id,
            region=self.config.region,
            tags=self.config.tags,
        )

        self.container.create()

    def _create_storage(self) -> None:
        """Create object storage bucket."""
        logger.debug("Creating object storage component")

        self.storage = ObjectStorageBucket(
            name="evalap-storage",
            environment=self.config.environment,
            config=self.config.storage,
            project_id=self.config.project_id,
            region=self.config.region,
            tags=self.config.tags,
        )

        self.storage.create()

    def _export_outputs(self) -> None:
        """Export stack outputs for API endpoint, database host, and storage bucket name."""
        logger.debug("Exporting stack outputs")

        # Container outputs
        if self.container:
            container_outputs = self.container.get_outputs()
            pulumi_helpers.export_output(
                "api_endpoint",
                self.container.get_endpoint(),
                "API container endpoint URL",
            )
            pulumi_helpers.export_output(
                "container_id",
                container_outputs.get("container_id"),
                "Container ID",
            )
            pulumi_helpers.export_output(
                "namespace_id",
                container_outputs.get("namespace_id"),
                "Container namespace ID",
            )

        # Database outputs
        if self.database:
            database_outputs = self.database.get_outputs()
            pulumi_helpers.export_output(
                "database_name",
                database_outputs.get("database_name"),
                "Database name",
            )
            pulumi_helpers.export_output(
                "database_username",
                database_outputs.get("username"),
                "Database username",
            )
            pulumi_helpers.export_output(
                "database_connection_string",
                self.database.get_connection_string(),
                "PostgreSQL connection string template (requires endpoint from Scaleway console)",
            )
            pulumi_helpers.export_output(
                "database_instance_id",
                database_outputs.get("instance_id"),
                "Database instance ID",
            )

        # Storage outputs
        if self.storage:
            storage_outputs = self.storage.get_outputs()
            pulumi_helpers.export_output(
                "storage_bucket_name",
                self.storage.get_bucket_name(),
                "Object storage bucket name",
            )
            pulumi_helpers.export_output(
                "storage_bucket_endpoint",
                self.storage.get_bucket_endpoint(),
                "Object storage bucket endpoint URL",
            )
            pulumi_helpers.export_output(
                "storage_bucket_region",
                storage_outputs.get("bucket_region"),
                "Object storage bucket region",
            )

        logger.info("Stack outputs exported successfully")

    def get_container(self) -> Optional[ServerlessContainer]:
        """Get container component."""
        return self.container

    def get_database(self) -> Optional[DatabaseInstance]:
        """Get database component."""
        return self.database

    def get_storage(self) -> Optional[ObjectStorageBucket]:
        """Get storage component."""
        return self.storage
