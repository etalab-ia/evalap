"""Serverless Container component for Scaleway Containers."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

import pulumi
import pulumiverse_scaleway as scaleway

from infra.components import BaseComponent
from infra.config.models import ContainerConfig
from infra.utils import pulumi_helpers, scaleway_helpers, validation

if TYPE_CHECKING:
    from infra.components.secret_manager import SecretManager

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
        secret_manager: Optional[SecretManager] = None,
        secret_mappings: Optional[dict[str, str]] = None,
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
            secret_manager: Optional SecretManager component for secret injection
            secret_mappings: Optional mapping of secret names to env var names.
                Format: {"secret_name": "ENV_VAR_NAME"}
                If provided with secret_manager, secrets will be injected as
                secret environment variables.
        """
        super().__init__(name, environment, tags, opts)
        self.config = config
        self.image_uri = image_uri
        self.project_id = project_id
        self.region = region
        self.secret_manager = secret_manager
        self.secret_mappings = secret_mappings or {}

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

        # Prepare secret environment variables
        secret_env_vars = self._build_secret_environment_variables()

        # Build container arguments
        container_args: dict[str, Any] = {
            "namespace_id": self.namespace.id,
            "name": container_name,
            "registry_image": self.image_uri,
            "port": self.config.port,
            "cpu_limit": self.config.cpu,
            "memory_limit": self.config.memory,
            "max_concurrency": self.config.max_concurrency,
            "timeout": self.config.timeout,
            "environment_variables": env_vars,
            "privacy": "public",
            "protocol": "http1",
            "deploy": True,
            "description": f"Container for {self.name} in {self.environment}",
            "opts": self.opts,
        }

        # Add secret environment variables if any
        if secret_env_vars:
            container_args["secret_environment_variables"] = secret_env_vars
            logger.debug(f"Injecting {len(secret_env_vars)} secret environment variables")

        self.container = scaleway.containers.Container(
            f"{self.name}-container",
            **container_args,
        )

    def _build_secret_environment_variables(self) -> dict[str, str]:
        """
        Build secret environment variables from config and secret manager.

        Combines secrets from:
        1. ContainerConfig.secret_environment_variables (direct values)
        2. SecretManager mappings (if secret_manager and secret_mappings provided)

        Returns:
            dict[str, str]: Combined secret environment variables
        """
        secret_env_vars: dict[str, str] = {}

        # Add secrets from config (direct values)
        secret_env_vars.update(self.config.secret_environment_variables)

        # Add secrets from SecretManager if available
        if self.secret_manager and self.secret_mappings:
            for secret_name, env_var_name in self.secret_mappings.items():
                try:
                    # Get the secret config to retrieve the data
                    # Note: This retrieves the secret data from the SecretConfig
                    # which is stored in Pulumi state (encrypted)
                    secret_config = self._get_secret_config(secret_name)
                    if secret_config:
                        secret_env_vars[env_var_name] = secret_config.data
                        logger.debug(f"Mapped secret '{secret_name}' to env var '{env_var_name}'")
                except KeyError:
                    logger.warning(
                        f"Secret '{secret_name}' not found in SecretManager. "
                        f"Available secrets: {list(self.secret_manager.secrets.keys())}"
                    )

        return secret_env_vars

    def _get_secret_config(self, secret_name: str) -> Any:
        """
        Get the SecretConfig for a given secret name from the SecretManager.

        Args:
            secret_name: Name of the secret

        Returns:
            SecretConfig if found, None otherwise
        """
        if not self.secret_manager:
            return None

        for config in self.secret_manager.configs:
            if config.name == secret_name:
                return config
        return None

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
