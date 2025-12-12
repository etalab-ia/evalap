"""Container Registry component for Scaleway Container Registry."""

import logging
from typing import Any, Optional

import pulumi
import pulumiverse_scaleway as scaleway

from infra.components import BaseComponent
from infra.utils import pulumi_helpers, scaleway_helpers

logger = logging.getLogger(__name__)


class ContainerRegistry(BaseComponent):
    """
    Container Registry component for storing Docker images.

    Manages Scaleway Container Registry namespace.
    """

    def __init__(
        self,
        name: str,
        environment: str,
        project_id: str,
        region: str = "fr-par",
        is_public: bool = False,
        tags: Optional[dict[str, str]] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """
        Initialize ContainerRegistry component.

        Args:
            name: Component name
            environment: Environment (dev, staging, production)
            project_id: Scaleway project ID
            region: Scaleway region (default: fr-par)
            is_public: Whether the registry is public (default: False)
            tags: Optional tags for resources
            opts: Optional Pulumi resource options
        """
        super().__init__(name, environment, tags, opts)
        self.project_id = project_id
        self.region = region
        self.is_public = is_public

        # Initialize resource references
        self.namespace: Optional[scaleway.registry.Namespace] = None

    def create(self) -> None:
        """Create the container registry namespace."""
        try:
            pulumi_helpers.log_resource_creation(
                "ContainerRegistry",
                self.name,
                environment=self.environment,
                is_public=self.is_public,
            )

            self._create_namespace()

            logger.info(f"ContainerRegistry '{self.name}' created successfully")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"ContainerRegistry.create({self.name})")

    def _create_namespace(self) -> None:
        """Create the registry namespace."""
        namespace_name = scaleway_helpers.format_resource_name(f"{self.name}-registry", self.environment)

        logger.debug(f"Creating registry namespace: {namespace_name}")

        self.namespace = scaleway.registry.Namespace(
            f"{self.name}-namespace",
            name=namespace_name,
            project_id=self.project_id,
            region=self.region,
            is_public=self.is_public,
            description=f"Container registry for {self.name} in {self.environment}",
            opts=self.opts,
        )

    def get_outputs(self) -> dict[str, Any]:
        """
        Get component outputs.

        Returns:
            dict: Dictionary containing:
                - namespace_id: Registry namespace ID
                - endpoint: Registry endpoint
        """
        if not self.namespace:
            return {}

        return {
            "namespace_id": self.namespace.id,
            "endpoint": self.namespace.endpoint,
        }

    def get_endpoint(self) -> pulumi.Output:
        """
        Get registry endpoint.

        Returns:
            pulumi.Output: Registry endpoint
        """
        if not self.namespace:
            raise ValueError("Namespace not created yet")
        return self.namespace.endpoint
