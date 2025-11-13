"""Serverless Container component for Scaleway Containers."""

import logging
from typing import Any, Optional

import pulumi
import pulumiverse_scaleway as scaleway

from infra.components import BaseComponent
from infra.config.models import ContainerConfig
from infra.utils import pulumi_helpers, scaleway_helpers, validation

logger = logging.getLogger(__name__)


class ServerlessContainer(BaseComponent):
    """
    Serverless Container component for deploying containerized applications.

    Manages container namespace, container definitions, health checks, and endpoint exposure.
    """

    def __init__(
        self,
        name: str,
        environment: str,
        config: ContainerConfig,
        image_uri: str,
        project_id: str,
        region: str = "fr-par",
        tags: Optional[dict[str, str]] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """
        Initialize ServerlessContainer component.

        Args:
            name: Component name
            environment: Environment (dev, staging, production)
            config: ContainerConfig with CPU, memory, and other settings
            image_uri: Container image URI (e.g., rg.fr-par.scw.cloud/my-image:latest)
            project_id: Scaleway project ID
            region: Scaleway region (default: fr-par)
            tags: Optional tags for resources
            opts: Optional Pulumi resource options
        """
        super().__init__(name, environment, tags, opts)
        self.config = config
        self.image_uri = image_uri
        self.project_id = project_id
        self.region = region

        # Validate configuration
        validation.validate_container_config(config.cpu, config.memory)

        # Initialize resource references
        self.namespace: Optional[scaleway.ContainerNamespace] = None
        self.container: Optional[scaleway.Container] = None

    def create(self) -> None:
        """Create the serverless container infrastructure."""
        try:
            pulumi_helpers.log_resource_creation(
                "ServerlessContainer",
                self.name,
                environment=self.environment,
                cpu=self.config.cpu,
                memory=self.config.memory,
            )

            # Create container namespace
            self._create_namespace()

            # Create container
            self._create_container()

            logger.info(f"ServerlessContainer '{self.name}' created successfully")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"ServerlessContainer.create({self.name})")

    def _create_namespace(self) -> None:
        """Create container namespace."""
        namespace_name = scaleway_helpers.format_resource_name(f"{self.name}-ns", self.environment)

        logger.debug(f"Creating container namespace: {namespace_name}")

        self.namespace = scaleway.containers.Namespace(
            f"{self.name}-namespace",
            name=namespace_name,
            project_id=self.project_id,
            region=self.region,
            description=f"Container namespace for {self.name} in {self.environment}",
            opts=self.opts,
        )

    def _create_container(self) -> None:
        """Create container with health checks and endpoint exposure."""
        if not self.namespace:
            raise ValueError("Namespace must be created before container")

        container_name = scaleway_helpers.format_resource_name(self.name, self.environment)

        logger.debug(f"Creating container: {container_name}")

        # Prepare environment variables
        env_vars = self.config.environment_variables.copy()
        env_vars.setdefault("LOG_LEVEL", "info")

        self.container = scaleway.containers.Container(
            f"{self.name}-container",
            namespace_id=self.namespace.id,
            name=container_name,
            registry_image=self.image_uri,
            port=self.config.port,
            cpu_limit=self.config.cpu,
            memory_limit=self.config.memory,
            max_concurrency=self.config.max_concurrency,
            timeout=self.config.timeout,
            environment_variables=env_vars,
            privacy="public",
            protocol="http1",
            deploy=True,
            description=f"Container for {self.name} in {self.environment}",
            opts=self.opts,
        )

    def get_outputs(self) -> dict[str, Any]:
        """
        Get component outputs.

        Returns:
            dict: Dictionary containing:
                - namespace_id: Container namespace ID
                - container_id: Container ID
                - endpoint: Container endpoint URL
                - image_uri: Container image URI
        """
        if not self.container or not self.namespace:
            return {}

        return {
            "namespace_id": self.namespace.id,
            "container_id": self.container.id,
            "endpoint": self.container.domain_name,
            "image_uri": self.image_uri,
            "cpu": self.config.cpu,
            "memory": self.config.memory,
        }

    def get_endpoint(self) -> pulumi.Output:
        """
        Get container endpoint URL.

        Returns:
            pulumi.Output: Container endpoint URL
        """
        if not self.container:
            raise ValueError("Container not created yet")
        return self.container.domain_name

    def get_namespace_id(self) -> pulumi.Output:
        """
        Get container namespace ID.

        Returns:
            pulumi.Output: Namespace ID
        """
        if not self.namespace:
            raise ValueError("Namespace not created yet")
        return self.namespace.id

    def get_container_id(self) -> pulumi.Output:
        """
        Get container ID.

        Returns:
            pulumi.Output: Container ID
        """
        if not self.container:
            raise ValueError("Container not created yet")
        return self.container.id
