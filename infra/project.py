"""Pulumi project setup and provider configuration."""

import logging

from infra.config.provider import get_provider_config, get_scaleway_provider, validate_provider_config

logger = logging.getLogger(__name__)


def setup_project() -> dict:
    """
    Set up the Pulumi project with Scaleway provider.

    Returns:
        dict: Dictionary containing provider configuration and provider instance

    Raises:
        ValueError: If provider configuration is invalid
    """
    # Get provider configuration
    config = get_provider_config()

    # Validate configuration
    try:
        validate_provider_config(config)
        logger.info("Provider configuration validated successfully")
    except ValueError as e:
        logger.error(f"Provider configuration validation failed: {e}")
        raise

    # Create and store provider
    provider = get_scaleway_provider()
    logger.info(f"Scaleway provider initialized for region: {config['region']}")

    return {"config": config, "provider": provider}


def get_stack_name() -> str:
    """
    Get the current Pulumi stack name.

    Returns:
        str: Stack name
    """
    import pulumi

    return pulumi.get_stack()


def get_project_name() -> str:
    """
    Get the current Pulumi project name.

    Returns:
        str: Project name
    """
    import pulumi

    return pulumi.get_project()


def initialize_logging(level: str = "INFO") -> None:
    """
    Initialize logging for the infrastructure project.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info(f"Logging initialized at level: {level}")
