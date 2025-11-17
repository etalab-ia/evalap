"""Scaleway provider configuration with credential handling."""

import os

import pulumi
import pulumiverse_scaleway as scaleway


def get_scaleway_provider() -> scaleway.Provider:
    """
    Create and return a Scaleway provider configured from environment variables.

    Returns:
        scaleway.Provider: Configured Scaleway provider instance

    Raises:
        ValueError: If required credentials are not available
    """
    # Get credentials from environment variables
    access_key = os.getenv("SCW_ACCESS_KEY")
    secret_key = os.getenv("SCW_SECRET_KEY")
    project_id = os.getenv("SCW_PROJECT_ID")
    region = os.getenv("SCW_REGION", "fr-par")

    if not access_key:
        raise ValueError("SCW_ACCESS_KEY environment variable not set")
    if not secret_key:
        raise ValueError("SCW_SECRET_KEY environment variable not set")
    if not project_id:
        raise ValueError("SCW_PROJECT_ID environment variable not set")

    # Create provider with explicit credentials
    provider = scaleway.Provider(
        "scaleway",
        access_key=access_key,
        secret_key=secret_key,
        project_id=project_id,
        region=region,
    )

    return provider


def get_provider_config() -> dict:
    """
    Get provider configuration from Pulumi config.

    Returns:
        dict: Provider configuration with region and credentials info
    """
    config = pulumi.Config()

    return {
        "region": config.get("scaleway:region") or os.getenv("SCW_REGION", "fr-par"),
        "project_id": config.get("scaleway:project_id") or os.getenv("SCW_PROJECT_ID"),
        "access_key": config.get_secret("scaleway:access_key") or os.getenv("SCW_ACCESS_KEY"),
        "secret_key": config.get_secret("scaleway:secret_key") or os.getenv("SCW_SECRET_KEY"),
    }


def validate_provider_config(config: dict) -> bool:
    """
    Validate that all required provider configuration is present.

    Args:
        config: Provider configuration dictionary

    Returns:
        bool: True if configuration is valid

    Raises:
        ValueError: If required configuration is missing
    """
    required_keys = ["region", "project_id", "access_key", "secret_key"]

    for key in required_keys:
        if not config.get(key):
            raise ValueError(f"Missing required provider configuration: {key}")

    return True
