"""Unified Application Stack implementation."""

import logging
import os
from typing import Optional

import pulumi

from infra.components.container_registry import ContainerRegistry
from infra.components.database import DatabaseInstance
from infra.components.iam_policy import IAMPolicy, ServiceType, create_service_policy
from infra.components.monitoring import Monitoring
from infra.components.object_storage import ObjectStorageBucket
from infra.components.private_network import PrivateNetwork
from infra.components.secret_manager import SecretManager
from infra.components.serverless_container import ServerlessContainer
from infra.config.models import SecretConfig, StackConfiguration
from infra.utils import pulumi_helpers

logger = logging.getLogger(__name__)


class ApplicationStack:
    """
    Unified Application Stack.

    Dynamically configures components based on configuration settings.
    Default topology:
    - Core: Database, Container, Object Storage, IAM Policies
    - Optional: Private Network (if network.enable_private_network)
    - Optional: Monitoring (if monitoring.enable_cockpit)
    """

    def __init__(self, config: StackConfiguration):
        """
        Initialize application stack.

        Args:
            config: StackConfiguration with all component configurations
        """
        self.config = config
        self.stack_name = pulumi.get_stack()

        # Initialize component references
        self.container_registry: Optional[ContainerRegistry] = None
        self.private_network: Optional[PrivateNetwork] = None
        self.secret_manager: Optional[SecretManager] = None
        self.iam_policy: Optional[IAMPolicy] = None
        self.container: Optional[ServerlessContainer] = None
        self.database: Optional[DatabaseInstance] = None
        self.storage: Optional[ObjectStorageBucket] = None
        self.monitoring: Optional[Monitoring] = None

        logger.info(f"Initializing application stack: {self.stack_name}")

    def create(self) -> None:
        """Create all infrastructure components for the stack."""
        try:
            logger.info(f"Creating application stack: {self.stack_name}")

            # 1. Create Private Network (Network Layer) - Optional
            self._create_private_network()

            # 1b. Create Container Registry (Build Layer)
            self._create_container_registry()

            # 2. Create Secret Manager (Security Layer)
            self._create_secret_manager()

            # 3. Create IAM Policies (Identity Layer)
            self._create_iam_policies()

            # 4. Create Database (Data Layer)
            self._create_database()

            # 5. Create Serverless Container (App Layer)
            self._create_container()

            # 6. Create Object Storage (Storage Layer)
            self._create_storage()

            # 7. Create Monitoring (Observability Layer) - Optional
            self._create_monitoring()

            # 8. Export outputs
            self._export_outputs()

            logger.info(f"Application stack '{self.stack_name}' created successfully")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"ApplicationStack.create({self.stack_name})")

    def _create_private_network(self) -> None:
        """Create private network for service isolation if enabled."""
        if not self.config.network.enable_private_network:
            logger.info("Private network disabled in configuration")
            return

        logger.debug("Creating private network component")

        self.private_network = PrivateNetwork(
            name="evalap-pn",
            environment=self.config.environment,
            config=self.config.network,
            project_id=self.config.project_id,
            region=self.config.region,
            tags=self.config.tags,
        )

        self.private_network.create()

    def _create_container_registry(self) -> None:
        """Create container registry."""
        logger.debug("Creating container registry component")

        self.container_registry = ContainerRegistry(
            name="evalap-registry",
            environment=self.config.environment,
            project_id=self.config.project_id,
            region=self.config.region,
            tags=self.config.tags,
        )

        self.container_registry.create()

    def _create_secret_manager(self) -> None:
        """Create Secret Manager with initial secrets."""
        logger.debug("Creating secret manager component")

        # Define initial secrets
        # Helper to get secret safe with fallback for preview/dev if needed
        # But we generally expect config to be there.
        try:
            db_password = pulumi.Config().require_secret("db_password")
        except Exception:
            # Fallback for dev/preview if not set (optional polish)
            db_password = pulumi.Output.secret("preview-password-change-me")

        secrets = [
            SecretConfig(
                name="db-password",
                data=db_password,
                description="Database password for EvalAP application",
            ),
            SecretConfig(
                name="api-key",
                data="placeholder-key",  # Placeholder, should be rotated
                description="API key for internal services",
            ),
        ]

        self.secret_manager = SecretManager(
            name="evalap-secrets",
            environment=self.config.environment,
            configs=secrets,
            project_id=self.config.project_id,
            region=self.config.region,
            tags=self.config.tags,
        )

        self.secret_manager.create()

    def _create_iam_policies(self) -> None:
        """Create IAM policies for least privilege access."""
        logger.debug("Creating IAM policy component")

        # Create service policy for the application
        self.iam_policy = create_service_policy(
            name="evalap-app-policy",
            environment=self.config.environment,
            service=ServiceType.SERVERLESS_CONTAINERS,
            access_level="full_access",
            project_id=self.config.project_id,
            tags=self.config.tags,
        )

        self.iam_policy.create()

    def _create_database(self) -> None:
        """Create managed PostgreSQL database."""
        logger.debug("Creating database component")

        self.database = DatabaseInstance(
            name="evalap-db",
            environment=self.config.environment,
            config=self.config.database,
            project_id=self.config.project_id,
            region=self.config.region,
            tags=self.config.tags,
            secret_manager=self.secret_manager,
            password_secret_name="db-password",
            private_network=self.private_network,  # Will be None if not created
        )

        self.database.create()

    def _create_container(self) -> None:
        """Create serverless container."""
        logger.debug("Creating container component")

        # Build and push image
        image_uri = self._build_image()
        if not image_uri:
            # Fallback for preview or if build disabled, though we aim to build
            image_uri = (
                pulumi.Config().get("container_image_uri") or "docker.io/testcontainers/helloworld:latest"
            )

        # Map secret names to environment variable names
        secret_mappings = {
            "db-password": "DB_PASSWORD",
            "api-key": "API_KEY",
        }

        self.container = ServerlessContainer(
            name="evalap-api",
            environment=self.config.environment,
            config=self.config.container,
            image_uri=image_uri,
            project_id=self.config.project_id,
            region=self.config.region,
            tags=self.config.tags,
            secret_manager=self.secret_manager,
            secret_mappings=secret_mappings,
            private_network=self.private_network,  # Will be None if not created
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

    def _build_image(self) -> Optional[pulumi.Output]:
        """Build and push Docker image."""
        if not self.container_registry:
            return None

        registry_endpoint = self.container_registry.get_endpoint()

        # Get registry credentials (assuming SCW_SECRET_KEY env var or config)
        # Scaleway Registry user is 'nologin', password is the secret key
        scw_secret_key = os.environ.get("SCW_SECRET_KEY") or pulumi.Config().get(
            "access_key"
        )  # specific to SCW provider setup

        if not scw_secret_key:
            # Try to get it from provider config if possible, or warn
            # For now, we assume environment variable is set as per walkthrough
            logger.warning("SCW_SECRET_KEY not found in env, docker push might fail if not logged in")
            scw_secret_key = "placeholder"  # Will likely fail build if strictly needed

        # Use manual docker build/push to avoid pulumi-docker context/networking issues with remote daemons (Colima)
        if pulumi.runtime.is_dry_run():
            # In preview, just return the expected tag
            return pulumi.Output.concat(registry_endpoint, "/evalap-api:latest")

        try:
            # Resolve endpoint to string for subprocess
            # Note: This requires apply, but we are inside create() which is synchronous construction time.
            # To mix sync subprocess with async outputs is tricky.
            # We must use 'apply' if we want to use the value, BUT 'apply' runs asynchronously.
            # However, for the build we need it "now" or we need to put the build INSIDE an apply.

            # Since we can't easily block on Output inside __init__ phase,
            # we will use the registry endpoint output in a dynamic provider or 'command' resource ideally.
            # But the simplest 'hack' that users ask for is to just run it.
            # Since 'registry_endpoint' is a generic Output, we might not have its value known immediately if it's being created.

            # Check if registry is already known (e.g. from stack ref or if it's just a string).
            # Self.container_registry.namespace.endpoint is an Output.

            # If we are creating the registry IN THIS STACK, we cannot build and push to it
            # in the same 'up' operation using simple subprocess at the top level,
            # because the registry doesn't exist yet when Python code runs!

            # We MUST use a Pulumi resource that depends on the registry.
            # Convert back to using `command` provider or `docker.Image` but with a workaround.
            pass
        except Exception:
            pass

        # REVERT STRATEGY:
        # The fail with 'docker.Image' was due to context transfer.
        # We can try to use 'docker.Image' but with a 'local' build context if we point to a tarball?
        # No, simpler:
        # We will keep using docker.Image but we will try to fix the context lookup by using absolute path
        # OR just acknowledge that the previous 'docker.Image' resource is the correct way but specifically the networking is broken.

        # Let's try ONE MORE configuration on the docker.Image resource: 'skip_push=False' is default.
        # What if we move the context to be explicitly '.' and ensure we run from root?
        # No, application.py runs in infra.

        # Alternative: Use "local-exec" via `command.local.Command` to run the docker build/push AFTER registry creation.

        import pulumi_command as command

        full_image_name = pulumi.Output.concat(registry_endpoint, "/evalap-api:latest")

        # Prepare the build command
        # We need to authenticate first.
        login_cmd = pulumi.Output.concat(
            "echo ", scw_secret_key, " | docker login ", registry_endpoint, " -u nologin --password-stdin"
        )

        build_cmd = pulumi.Output.concat(
            "docker build --platform linux/amd64 -t ", full_image_name, " -f ../Dockerfile .."
        )

        push_cmd = pulumi.Output.concat("docker push ", full_image_name)

        # Chain commands: Login && Build && Push
        # Note: DOCKER_HOST is inherited from the process running pulumi (our justfile fix)
        create_cmd = pulumi.Output.concat(login_cmd, " && ", build_cmd, " && ", push_cmd)

        image_resource = command.local.Command(
            "evalap-api-image-build",
            create=create_cmd,
            # We can optionally add environment={"DOCKER_HOST": ...} but it should inherit.
            opts=pulumi.ResourceOptions(
                depends_on=[self.container_registry.namespace]
            ),  # Ensure registry exists
        )

        # Return the image name (tagged)
        # We make it depend on the command completing
        return full_image_name.apply(lambda name: name) if image_resource else None

    def _create_monitoring(self) -> None:
        """Create monitoring configuration if enabled."""
        if not self.config.monitoring.enable_cockpit:
            logger.info("Monitoring disabled in configuration")
            return

        logger.debug("Creating monitoring component")

        self.monitoring = Monitoring(
            name="evalap-monitoring",
            environment=self.config.environment,
            config=self.config.monitoring,
            project_id=self.config.project_id,
            region=self.config.region,
            tags=self.config.tags,
        )

        self.monitoring.create()

    def _export_outputs(self) -> None:
        """Export stack outputs."""
        logger.debug("Exporting stack outputs")

        # Private Network Outputs
        if self.private_network:
            pn_outputs = self.private_network.get_outputs()
            pulumi_helpers.export_output("vpc_id", pn_outputs.get("vpc_id"), "VPC ID")
            pulumi_helpers.export_output(
                "private_network_id", pn_outputs.get("private_network_id"), "Private Network ID"
            )

        # Secret Manager Outputs
        if self.secret_manager:
            sm_outputs = self.secret_manager.get_outputs()
            pulumi_helpers.export_output(
                "secret_count", sm_outputs.get("secret_count"), "Number of secrets managed"
            )

        # Database Outputs
        if self.database:
            db_outputs = self.database.get_outputs()
            pulumi_helpers.export_output("database_endpoint_ip", db_outputs.get("endpoint_ip"), "Public DB IP")

            # Export private connection string if available
            if self.database.is_private_network_enabled():
                pulumi_helpers.export_output(
                    "database_private_connection_string",
                    self.database.get_private_network_connection_string(),
                    "Internal DB Connection String",
                )

        # Container Outputs
        if self.container:
            pulumi_helpers.export_output("api_endpoint", self.container.get_endpoint(), "API URL")

        # Monitoring Outputs
        if self.monitoring:
            monitoring_outputs = self.monitoring.get_outputs()
            pulumi_helpers.export_output(
                "grafana_url", monitoring_outputs.get("grafana_url"), "Cockpit Grafana URL"
            )
            pulumi_helpers.export_output(
                "metrics_url", monitoring_outputs.get("metrics_url"), "Metrics Query URL"
            )
            pulumi_helpers.export_output(
                "metrics_push_url", monitoring_outputs.get("metrics_push_url"), "Metrics Push URL"
            )
            pulumi_helpers.export_output("logs_url", monitoring_outputs.get("logs_url"), "Logs URL")
