"""Pulumi infrastructure entry point that instantiates the appropriate stack."""

import logging
import os
import sys

import pulumi

# Add parent directory to Python path to resolve infra module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infra.config.models import (
    ContainerConfig,
    DatabaseConfig,
    MonitoringConfig,
    NetworkConfig,
    StackConfiguration,
    StorageConfig,
)
from infra.stacks.application import ApplicationStack
from infra.utils import pulumi_helpers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_stack_configuration() -> StackConfiguration:
    """
    Load stack configuration from Pulumi config and environment.

    Returns:
        StackConfiguration: Complete stack configuration

    Raises:
        ValueError: If required configuration is missing
    """
    config = pulumi.Config()
    stack_name = pulumi.get_stack()

    logger.info(f"Loading configuration for stack: {stack_name}")

    # Get required configuration
    project_id = config.require("project_id")
    region = config.get("region") or "fr-par"
    environment = config.get("environment") or stack_name

    # Load container configuration
    container_config = ContainerConfig(
        cpu=config.get_int("container_cpu") or 1000,
        memory=config.get_int("container_memory") or 1024,
        max_concurrency=config.get_int("container_max_concurrency") or 80,
        timeout=config.get_int("container_timeout") or 300,
        environment_variables=config.get_object("container_env_vars") or {},
    )

    # Load database configuration
    database_config = DatabaseConfig(
        engine=config.get("database_engine") or "PostgreSQL-15",
        volume_size=config.get_int("database_volume_size") or 20,
        backup_retention_days=config.get_int("database_backup_retention_days") or 7,
        enable_backups=config.get_bool("database_enable_backups") or True,
        enable_high_availability=config.get_bool("database_enable_ha") or False,
        user_name=config.get("database_user_name") or "admin",
        database_name=config.get("database_name") or "evalap",
    )

    # Load storage configuration
    storage_config = StorageConfig(
        versioning_enabled=config.get_bool("storage_versioning_enabled") or True,
        lifecycle_expiration_days=config.get_int("storage_lifecycle_expiration_days"),
        acl=config.get("storage_acl") or "private",
        encryption_enabled=config.get_bool("storage_encryption_enabled") or True,
    )

    # Load network configuration
    network_config = NetworkConfig(
        enable_private_network=config.get_bool("network_enable_private") or False,
        cidr_block=config.get("network_cidr_block") or "10.0.0.0/16",
        enable_nat_gateway=config.get_bool("network_enable_nat") or False,
    )

    # Load monitoring configuration
    monitoring_config = MonitoringConfig(
        enable_cockpit=config.get_bool("monitoring_enable_cockpit") or True,
        metrics_retention_days=config.get_int("monitoring_metrics_retention_days") or 30,
        log_retention_days=config.get_int("monitoring_log_retention_days") or 30,
        enable_alerts=config.get_bool("monitoring_enable_alerts") or True,
        alert_email=config.get("monitoring_alert_email"),
    )

    # Load common tags
    tags = config.get_object("tags") or {}
    tags.setdefault("project", "evalap")
    tags.setdefault("managed-by", "pulumi")

    # Create stack configuration
    stack_config = StackConfiguration(
        stack_name=stack_name,
        environment=environment,
        region=region,
        project_id=project_id,
        container=container_config,
        database=database_config,
        storage=storage_config,
        network=network_config,
        monitoring=monitoring_config,
        tags=tags,
    )

    logger.info(f"Stack configuration loaded successfully for {stack_name}")
    return stack_config


def create_stack(config: StackConfiguration) -> None:
    """
    Create the appropriate stack based on Pulumi stack selection.

    Args:
        config: StackConfiguration with all component configurations

    Raises:
        ValueError: If stack type is not supported
    """
    stack_name = pulumi.get_stack()

    logger.info(f"Creating stack: {stack_name}")

    # Create unified application stack
    # The ApplicationStack adapts based on the configuration (e.g., enabling private network/monitoring)
    stack = ApplicationStack(config)
    stack.create()

    logger.info(f"Stack '{stack_name}' created successfully")


def main() -> None:
    """Main entry point for Pulumi infrastructure."""
    try:
        logger.info("Starting Pulumi infrastructure deployment")

        # Load configuration
        config = load_stack_configuration()

        # Create stack
        create_stack(config)

        logger.info("Pulumi infrastructure deployment completed successfully")
    except Exception as e:
        logger.error(f"Failed to create infrastructure: {str(e)}")
        pulumi_helpers.handle_error(e, "main")
        sys.exit(1)


if __name__ == "__main__":
    main()
