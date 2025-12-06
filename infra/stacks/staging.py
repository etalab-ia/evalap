"""Staging stack implementation with comprehensive security controls."""

import logging
from typing import Optional

import pulumi

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


class StagingStack:
    """
    Staging stack with security components.

    Combines:
    - PrivateNetwork for service isolation
    - SecretManager for credential management
    - IAMPolicy for least privilege access
    - ServerlessContainer for application
    - DatabaseInstance for data
    - ObjectStorageBucket for artifacts
    """

    def __init__(self, config: StackConfiguration):
        """
        Initialize staging stack.

        Args:
            config: StackConfiguration with all component configurations
        """
        self.config = config
        self.stack_name = pulumi.get_stack()

        # Initialize component references
        self.private_network: Optional[PrivateNetwork] = None
        self.secret_manager: Optional[SecretManager] = None
        self.iam_policy: Optional[IAMPolicy] = None
        self.container: Optional[ServerlessContainer] = None
        self.database: Optional[DatabaseInstance] = None
        self.storage: Optional[ObjectStorageBucket] = None
        self.monitoring: Optional[Monitoring] = None

        logger.info(f"Initializing staging stack: {self.stack_name}")

    def create(self) -> None:
        """Create all infrastructure components for the staging stack."""
        try:
            logger.info(f"Creating staging stack: {self.stack_name}")

            # 1. Create Private Network (Network Layer)
            self._create_private_network()

            # 2. Create Secret Manager (Security Layer)
            self._create_secret_manager()

            # 3. Create IAM Policies (Identity Layer)
            self._create_iam_policies()

            # 4. Create Database (Data Layer) - depends on Private Network and Secret Manager
            self._create_database()

            # 5. Create Serverless Container (App Layer) - depends on Private Network and Secret Manager
            self._create_container()

            # 6. Create Object Storage (Storage Layer)
            self._create_storage()

            # 7. Create Monitoring (Observability Layer)
            self._create_monitoring()

            # 8. Export outputs
            self._export_outputs()

            logger.info(f"Staging stack '{self.stack_name}' created successfully")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"StagingStack.create({self.stack_name})")

    def _create_private_network(self) -> None:
        """Create private network for service isolation."""
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

    def _create_secret_manager(self) -> None:
        """Create Secret Manager with initial secrets."""
        logger.debug("Creating secret manager component")

        # Define initial secrets
        # In a real scenario, values should come from Pulumi config secrets or be generated
        db_password = pulumi.Config().require_secret("db_password")

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
            access_level="full_access",  # Needs full access to manage its own container lifecycle if needed, or adjust
            project_id=self.config.project_id,
            tags=self.config.tags,
        )

        self.iam_policy.create()

    def _create_database(self) -> None:
        """Create managed PostgreSQL database connected to private network and using managed secrets."""
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
            private_network=self.private_network,
        )

        self.database.create()

    def _create_container(self) -> None:
        """Create serverless container connected to private network and using secrets."""
        logger.debug("Creating container component")

        image_uri = pulumi.Config().get("container_image_uri") or "docker.io/testcontainers/helloworld:latest"

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
            private_network=self.private_network,
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

    def _create_monitoring(self) -> None:
        """Create monitoring configuration."""
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
