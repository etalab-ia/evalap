"""Monitoring component for Scaleway Cockpit."""

import logging
from typing import Optional

import pulumi
import pulumiverse_scaleway as scaleway

from infra.components import BaseComponent
from infra.config.models import MonitoringConfig
from infra.utils import pulumi_helpers, scaleway_helpers

logger = logging.getLogger(__name__)


class Monitoring(BaseComponent):
    """
    Monitoring component using Scaleway Cockpit.

    Manages:
    - Cockpit retrieval (ensures the project's cockpit is active)
    - Alert Manager configuration (if supported via provider, otherwise placeholders)
    - Token creation for Grafana/Metrics pushing
    """

    def __init__(
        self,
        name: str,
        environment: str,
        config: MonitoringConfig,
        project_id: str,
        region: str = "fr-par",
        tags: Optional[dict[str, str]] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """
        Initialize Monitoring component.

        Args:
            name: Component name
            environment: Environment (dev, staging, production)
            config: MonitoringConfig
            project_id: Scaleway project ID
            region: Scaleway region
            tags: Optional tags
            opts: Optional Pulumi resource options
        """
        super().__init__(name, environment, tags, opts)
        self.config = config
        self.project_id = project_id
        self.region = region

        # Initialize resource references
        self.metrics_source: Optional[scaleway.observability.Source] = None
        self.logs_source: Optional[scaleway.observability.Source] = None
        self.token: Optional[scaleway.observability.Token] = None
        self.alert_manager: Optional[scaleway.observability.AlertManager] = None

    def create(self) -> None:
        """Create monitoring infrastructure."""
        if not self.config.enable_cockpit:
            logger.info(f"Cockpit monitoring disabled for '{self.name}'")
            return

        try:
            pulumi_helpers.log_resource_creation(
                "Monitoring",
                self.name,
                environment=self.environment,
            )

            # 1. Create Data Sources (Metrics, Logs)
            self._create_sources()

            # 2. Create Token for metrics/logs writing if needed
            self._create_token()

            # 3. Create Alert Manager
            self._create_alert_manager()

            logger.info(f"Monitoring '{self.name}' created successfully")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"Monitoring.create({self.name})")

    def _create_sources(self) -> None:
        """Create Cockpit data sources."""
        # Metrics Source
        self.metrics_source = scaleway.observability.Source(
            f"{self.name}-metrics",
            project_id=self.project_id,
            type="metrics",
            retention_days=self.config.metrics_retention_days,
            opts=self.opts,
        )

        # Logs Source
        self.logs_source = scaleway.observability.Source(
            f"{self.name}-logs",
            project_id=self.project_id,
            type="logs",
            retention_days=self.config.log_retention_days,
            opts=self.opts,
        )

    def _create_token(self) -> None:
        """Create a token for writing metrics/logs."""
        if not self.metrics_source:
            return

        token_name = scaleway_helpers.format_resource_name("metrics-token", self.environment)

        self.token = scaleway.observability.Token(
            f"{self.name}-token",
            project_id=self.project_id,
            name=token_name,
            scopes=scaleway.observability.TokenScopesArgs(
                query_metrics=True,
                write_metrics=True,
                query_logs=True,
                write_logs=True,
            ),
            # Set parent to metrics_source for logical grouping, or just opts
            opts=pulumi.ResourceOptions(parent=self.metrics_source) if self.opts else None,
        )

    def _create_alert_manager(self) -> None:
        """Create Alert Manager and configure contact points."""
        if not self.config.enable_alerts:
            return

        contact_points = []
        if self.config.alert_email:
            contact_points.append(
                scaleway.observability.AlertManagerContactPointArgs(email=self.config.alert_email)
            )

        self.alert_manager = scaleway.observability.AlertManager(
            f"{self.name}-alert-manager",
            project_id=self.project_id,
            enable_managed_alerts=True,
            contact_points=contact_points,
            opts=self.opts,
        )

    def get_outputs(self) -> dict[str, Optional[str]]:
        """Get component outputs."""
        outputs = {}

        if self.metrics_source:
            # Source.url is typically the query endpoint
            outputs["metrics_url"] = self.metrics_source.url
            # Source.push_url is the ingestion endpoint
            outputs["metrics_push_url"] = self.metrics_source.push_url

        if self.logs_source:
            outputs["logs_url"] = self.logs_source.url

        # Grafana URL is standard for the region/project, or we can try to find it
        # For now, we omit it or construct it manually if needed,
        # but the Source resource doesn't expose it directly as per CLI help.
        # We can construct it: https://cockpit.fr-par.scw.cloud/ usually
        outputs["grafana_url"] = pulumi.Output.from_input("https://cockpit.fr-par.scw.cloud")

        return outputs
