"""Object Storage Bucket component for Scaleway Object Storage."""

import logging
from typing import Any, Optional

import pulumi
import pulumi_scaleway as scaleway

from infra.components import BaseComponent
from infra.config.models import StorageConfig
from infra.utils import pulumi_helpers, scaleway_helpers, validation

logger = logging.getLogger(__name__)


class ObjectStorageBucket(BaseComponent):
    """
    Object Storage Bucket component for Scaleway Object Storage.

    Manages bucket creation, versioning, lifecycle rules, and access control.
    """

    def __init__(
        self,
        name: str,
        environment: str,
        config: StorageConfig,
        project_id: str,
        region: str = "fr-par",
        tags: Optional[dict[str, str]] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """
        Initialize ObjectStorageBucket component.

        Args:
            name: Component name
            environment: Environment (dev, staging, production)
            config: StorageConfig with versioning, lifecycle, and ACL settings
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
        validation.validate_storage_config(config)

        # Initialize resource references
        self.bucket: Optional[scaleway.ObjectBucket] = None

    def create(self) -> None:
        """Create the object storage bucket infrastructure."""
        try:
            pulumi_helpers.log_resource_creation(
                "ObjectStorageBucket",
                self.name,
                environment=self.environment,
                versioning=self.config.versioning_enabled,
                acl=self.config.acl,
            )

            # Create bucket
            self._create_bucket()

            # Configure versioning if enabled
            if self.config.versioning_enabled:
                self._configure_versioning()

            # Configure lifecycle rules if expiration is set
            if self.config.lifecycle_expiration_days:
                self._configure_lifecycle()

            logger.info(f"ObjectStorageBucket '{self.name}' created successfully")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"ObjectStorageBucket.create({self.name})")

    def _create_bucket(self) -> None:
        """Create object storage bucket."""
        bucket_name = scaleway_helpers.format_resource_name(self.name, self.environment)

        # Validate bucket name
        validation.validate_bucket_name(bucket_name)

        logger.debug(f"Creating object storage bucket: {bucket_name}")

        # Prepare bucket arguments
        bucket_args = scaleway.ObjectBucketArgs(
            name=bucket_name,
            region=self.region,
            acl=self.config.acl,
            tags=scaleway_helpers.create_resource_tags(
                self.environment, "object-storage", additional_tags=self.tags
            ),
        )

        # Add versioning if enabled
        if self.config.versioning_enabled:
            bucket_args.versioning = scaleway.ObjectBucketVersioningArgs(enabled=True)

        # Add lifecycle rules if expiration is set
        if self.config.lifecycle_expiration_days:
            bucket_args.lifecycle_rules = [
                scaleway.ObjectBucketLifecycleRuleArgs(
                    id="expire-old-objects",
                    enabled=True,
                    expiration=scaleway.ObjectBucketLifecycleRuleExpirationArgs(
                        days=self.config.lifecycle_expiration_days
                    ),
                )
            ]

        self.bucket = scaleway.ObjectBucket(
            f"{self.name}-bucket",
            args=bucket_args,
            opts=self.opts,
        )

    def _configure_versioning(self) -> None:
        """Configure object versioning."""
        # Versioning is now configured during bucket creation
        # This method is kept for compatibility but does nothing
        logger.debug("Versioning is configured during bucket creation")

    def _configure_lifecycle(self) -> None:
        """Configure lifecycle rules for object expiration."""
        # Lifecycle rules are now configured during bucket creation
        # This method is kept for compatibility but does nothing
        logger.debug("Lifecycle rules are configured during bucket creation")

    def get_outputs(self) -> dict[str, Any]:
        """
        Get component outputs.

        Returns:
            dict: Dictionary containing:
                - bucket_name: Bucket name
                - bucket_region: Bucket region
                - bucket_endpoint: Bucket endpoint URL
                - versioning_enabled: Whether versioning is enabled
                - acl: Access control level
        """
        if not self.bucket:
            return {}

        return {
            "bucket_name": self.bucket.bucket,
            "bucket_region": self.region,
            "bucket_endpoint": pulumi.Output.concat(
                "https://", self.bucket.bucket, ".s3.", self.region, ".scw.cloud"
            ),
            "versioning_enabled": self.config.versioning_enabled,
            "acl": self.config.acl,
            "encryption_enabled": self.config.encryption_enabled,
            "lifecycle_expiration_days": self.config.lifecycle_expiration_days,
        }

    def get_bucket_name(self) -> pulumi.Output:
        """
        Get bucket name.

        Returns:
            pulumi.Output: Bucket name
        """
        if not self.bucket:
            raise ValueError("Bucket not created yet")
        return self.bucket.bucket

    def get_bucket_endpoint(self) -> pulumi.Output:
        """
        Get bucket endpoint URL.

        Returns:
            pulumi.Output: Bucket endpoint URL
        """
        if not self.bucket:
            raise ValueError("Bucket not created yet")

        return pulumi.Output.concat("https://", self.bucket.bucket, ".s3.", self.region, ".scw.cloud")

    def get_bucket_region(self) -> str:
        """
        Get bucket region.

        Returns:
            str: Bucket region
        """
        return self.region
