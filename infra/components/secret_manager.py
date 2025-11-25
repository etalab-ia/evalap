"""Secret Manager component for Scaleway Secret Manager."""

import logging
from typing import Any, Optional

import pulumi
import pulumiverse_scaleway as scaleway

from infra.components import BaseComponent
from infra.config.models import SecretConfig
from infra.utils import pulumi_helpers, scaleway_helpers

logger = logging.getLogger(__name__)


class SecretManager(BaseComponent):
    """
    Secret Manager component for Scaleway Secret Manager.

    Manages secret creation, versioning, and credential storage.
    Secrets are stored with immutable versions - each update creates a new version.
    """

    def __init__(
        self,
        name: str,
        environment: str,
        configs: list[SecretConfig],
        project_id: str,
        region: str = "fr-par",
        tags: Optional[dict[str, str]] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """
        Initialize SecretManager component.

        Args:
            name: Component name
            environment: Environment (dev, staging, production)
            configs: List of SecretConfig objects defining secrets to create
            project_id: Scaleway project ID
            region: Scaleway region (default: fr-par)
            tags: Optional tags for resources
            opts: Optional Pulumi resource options
        """
        super().__init__(name, environment, tags, opts)
        self.configs = configs
        self.project_id = project_id
        self.region = region

        # Initialize resource references
        self.secrets: dict[str, scaleway.secrets.Secret] = {}
        self.versions: dict[str, scaleway.secrets.Version] = {}

    def create(self) -> None:
        """Create all secrets and their initial versions."""
        try:
            pulumi_helpers.log_resource_creation(
                "SecretManager",
                self.name,
                environment=self.environment,
                secret_count=len(self.configs),
            )

            for config in self.configs:
                self._create_secret(config)

            logger.info(f"SecretManager '{self.name}' created {len(self.configs)} secrets")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"SecretManager.create({self.name})")

    def _create_secret(self, config: SecretConfig) -> None:
        """
        Create a secret and its initial version.

        Args:
            config: SecretConfig with secret details
        """
        secret_name = scaleway_helpers.format_resource_name(config.name, self.environment)

        logger.debug(f"Creating secret: {secret_name}")

        # Create the secret container
        secret = scaleway.secrets.Secret(
            f"{self.name}-{config.name}",
            name=secret_name,
            description=config.description,
            path=config.path,
            project_id=self.project_id,
            region=self.region,
            protected=config.protected,
            type=config.secret_type,
            tags=self._format_tags_list(),
            opts=self.opts,
        )

        self.secrets[config.name] = secret

        # Create the initial version with the secret data
        # Use parent to establish dependency relationship
        version_opts = pulumi.ResourceOptions(parent=secret) if self.opts else None
        version = scaleway.secrets.Version(
            f"{self.name}-{config.name}-v1",
            secret_id=secret.id,
            data=config.data,
            description="Initial version",
            region=self.region,
            opts=version_opts,
        )

        self.versions[config.name] = version

        logger.debug(f"Created secret '{secret_name}' with initial version")

    def _format_tags_list(self) -> list[str]:
        """
        Format tags as a list of strings for Scaleway Secret Manager.

        Scaleway secrets use a list of strings for tags, not key-value pairs.

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
                - secrets: Dict of secret names to their IDs
                - secret_count: Number of secrets created
                - region: Region where secrets are stored
        """
        secret_ids = {}
        for name, secret in self.secrets.items():
            secret_ids[name] = secret.id

        return {
            "secrets": secret_ids,
            "secret_count": len(self.secrets),
            "region": self.region,
        }

    def get_secret_id(self, secret_name: str) -> pulumi.Output:
        """
        Get the ID of a specific secret.

        Args:
            secret_name: Name of the secret (as defined in SecretConfig)

        Returns:
            pulumi.Output: Secret ID

        Raises:
            KeyError: If secret name not found
        """
        if secret_name not in self.secrets:
            raise KeyError(f"Secret '{secret_name}' not found. Available: {list(self.secrets.keys())}")
        return self.secrets[secret_name].id

    def get_secret_version_id(self, secret_name: str) -> pulumi.Output:
        """
        Get the ID of the current version for a specific secret.

        Args:
            secret_name: Name of the secret (as defined in SecretConfig)

        Returns:
            pulumi.Output: Secret version ID

        Raises:
            KeyError: If secret name not found
        """
        if secret_name not in self.versions:
            raise KeyError(
                f"Secret version for '{secret_name}' not found. Available: {list(self.versions.keys())}"
            )
        return self.versions[secret_name].id

    def get_secret_for_container(self, secret_name: str, env_var_name: str) -> dict[str, pulumi.Output]:
        """
        Get secret reference formatted for serverless container environment variables.

        This returns the format needed for Scaleway Serverless Container
        secret environment variables.

        Args:
            secret_name: Name of the secret (as defined in SecretConfig)
            env_var_name: Environment variable name in the container

        Returns:
            dict: Secret environment variable configuration with:
                - key: Environment variable name
                - secret_id: Secret ID
                - secret_version: Version to use ("latest" or specific revision)

        Raises:
            KeyError: If secret name not found
        """
        if secret_name not in self.secrets:
            raise KeyError(f"Secret '{secret_name}' not found. Available: {list(self.secrets.keys())}")

        return {
            "key": env_var_name,
            "secret_id": self.secrets[secret_name].id,
            "secret_version": "latest",
        }

    def create_secret(self, config: SecretConfig) -> tuple[pulumi.Output, pulumi.Output]:
        """
        Create a single secret dynamically (after initial creation).

        This method allows adding secrets after the component is created.

        Args:
            config: SecretConfig with secret details

        Returns:
            tuple: (secret_id, version_id)
        """
        self._create_secret(config)
        return (
            self.secrets[config.name].id,
            self.versions[config.name].id,
        )

    def update_secret_version(
        self,
        secret_name: str,
        new_data: str,
        description: Optional[str] = None,
    ) -> pulumi.Output:
        """
        Create a new version for an existing secret.

        Note: In Pulumi, this creates a new Version resource. The old version
        remains immutable. For rotation, create a new version and update
        consumers to use the new version.

        Args:
            secret_name: Name of the secret to update
            new_data: New secret data
            description: Optional description for the new version

        Returns:
            pulumi.Output: New version ID

        Raises:
            KeyError: If secret name not found
        """
        if secret_name not in self.secrets:
            raise KeyError(f"Secret '{secret_name}' not found. Available: {list(self.secrets.keys())}")

        # Generate a unique version name
        version_count = len([k for k in self.versions.keys() if k.startswith(secret_name)])
        version_name = f"{self.name}-{secret_name}-v{version_count + 1}"

        new_version = scaleway.secrets.Version(
            version_name,
            secret_id=self.secrets[secret_name].id,
            data=new_data,
            description=description or f"Version {version_count + 1}",
            region=self.region,
            opts=pulumi.ResourceOptions(
                parent=self.secrets[secret_name],
            ),
        )

        # Update the tracked version
        self.versions[secret_name] = new_version

        logger.info(f"Created new version for secret '{secret_name}'")
        return new_version.id
