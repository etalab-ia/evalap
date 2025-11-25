"""Infrastructure configuration validation utilities."""

import re
from typing import Any

from infra.config.models import StackConfiguration
from infra.utils import scaleway_helpers


def validate_stack_configuration(config: StackConfiguration) -> bool:
    """
    Validate complete stack configuration.

    Args:
        config: StackConfiguration object to validate

    Returns:
        bool: True if valid

    Raises:
        ValueError: If configuration is invalid
    """
    # Validate container configuration
    validate_container_config(config.container.cpu, config.container.memory)

    # Validate database configuration
    validate_database_config(config.database.volume_size, config.database.backup_retention_days)

    # Validate storage configuration
    validate_storage_config(config.storage)

    # Validate network configuration
    validate_network_config(config.network)

    return True


def validate_container_config(cpu: int, memory: int) -> bool:
    """
    Validate container resource configuration.

    Args:
        cpu: CPU in millicores
        memory: Memory in MB

    Returns:
        bool: True if valid

    Raises:
        ValueError: If configuration is invalid
    """
    if not (100 <= cpu <= 4000):
        raise ValueError(f"CPU must be between 100-4000 millicores, got {cpu}")

    if not (128 <= memory <= 8192):
        raise ValueError(f"Memory must be between 128-8192 MB, got {memory}")

    # Validate CPU/memory combination
    scaleway_helpers.validate_cpu_memory_combination(cpu, memory)

    return True


def validate_database_config(volume_size: int, backup_retention: int) -> bool:
    """
    Validate database configuration.

    Args:
        volume_size: Volume size in GB
        backup_retention: Backup retention in days

    Returns:
        bool: True if valid

    Raises:
        ValueError: If configuration is invalid
    """
    if not (5 <= volume_size <= 500):
        raise ValueError(f"Volume size must be 5-500 GB, got {volume_size}")

    if not (1 <= backup_retention <= 365):
        raise ValueError(f"Backup retention must be 1-365 days, got {backup_retention}")

    return True


def validate_storage_config(storage_config: Any) -> bool:
    """
    Validate object storage configuration.

    Args:
        storage_config: Storage configuration object

    Returns:
        bool: True if valid

    Raises:
        ValueError: If configuration is invalid
    """
    if storage_config.acl not in ["private", "public-read", "authenticated-read"]:
        raise ValueError(
            f"Invalid ACL '{storage_config.acl}'. Must be one of: private, public-read, authenticated-read"
        )

    if storage_config.lifecycle_expiration_days is not None and storage_config.lifecycle_expiration_days < 1:
        raise ValueError(
            f"Lifecycle expiration must be >= 1 day, got {storage_config.lifecycle_expiration_days}"
        )

    return True


def validate_network_config(network_config: Any) -> bool:
    """
    Validate network configuration.

    Args:
        network_config: Network configuration object

    Returns:
        bool: True if valid

    Raises:
        ValueError: If configuration is invalid
    """
    if network_config.enable_private_network:
        # Validate CIDR block format
        cidr = network_config.cidr_block
        if not validate_cidr_block(cidr):
            raise ValueError(f"Invalid CIDR block: {cidr}")

    return True


def validate_cidr_block(cidr: str) -> bool:
    """
    Validate CIDR block format.

    Args:
        cidr: CIDR block string (e.g., 10.0.0.0/16)

    Returns:
        bool: True if valid

    Raises:
        ValueError: If CIDR is invalid
    """
    pattern = r"^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$"
    if not re.match(pattern, cidr):
        raise ValueError(f"Invalid CIDR format: {cidr}")

    # Validate IP octets
    ip_part = cidr.split("/")[0]
    octets = ip_part.split(".")
    for octet in octets:
        if not (0 <= int(octet) <= 255):
            raise ValueError(f"Invalid IP address in CIDR: {cidr}")

    # Validate prefix length
    prefix = int(cidr.split("/")[1])
    if not (0 <= prefix <= 32):
        raise ValueError(f"Invalid prefix length in CIDR: {cidr}")

    return True


def validate_resource_name(name: str, resource_type: str = "resource") -> bool:
    """
    Validate resource name.

    Args:
        name: Resource name
        resource_type: Type of resource

    Returns:
        bool: True if valid

    Raises:
        ValueError: If name is invalid
    """
    return scaleway_helpers.validate_resource_name(name, resource_type)


def validate_bucket_name(name: str) -> bool:
    """
    Validate bucket name.

    Args:
        name: Bucket name

    Returns:
        bool: True if valid

    Raises:
        ValueError: If name is invalid
    """
    return scaleway_helpers.validate_bucket_name(name)


def validate_database_name(name: str) -> bool:
    """
    Validate database name.

    Args:
        name: Database name

    Returns:
        bool: True if valid

    Raises:
        ValueError: If name is invalid
    """
    return scaleway_helpers.validate_database_name(name)


def validate_iam_policy(policy: dict) -> bool:
    """
    Validate IAM policy structure.

    Args:
        policy: IAM policy dictionary

    Returns:
        bool: True if valid

    Raises:
        ValueError: If policy is invalid
    """
    required_keys = ["Version", "Statement"]
    for key in required_keys:
        if key not in policy:
            raise ValueError(f"IAM policy missing required key: {key}")

    if not isinstance(policy["Statement"], list):
        raise ValueError("IAM policy Statement must be a list")

    for statement in policy["Statement"]:
        if "Effect" not in statement:
            raise ValueError("IAM policy Statement missing Effect")
        if statement["Effect"] not in ["Allow", "Deny"]:
            raise ValueError(f"Invalid Effect: {statement['Effect']}")

    return True


def validate_state_backend_config(
    bucket_name: str,
    region: str,
    endpoint: str,
) -> bool:
    """
    Validate Pulumi state backend configuration.

    Args:
        bucket_name: S3 bucket name
        region: Scaleway region
        endpoint: S3 endpoint URL

    Returns:
        bool: True if valid

    Raises:
        ValueError: If configuration is invalid
    """
    # Validate bucket name
    validate_bucket_name(bucket_name)

    # Validate region
    valid_regions = ["fr-par", "nl-ams", "pl-waw"]
    if region not in valid_regions:
        raise ValueError(f"Invalid region: {region}. Must be one of {valid_regions}")

    # Validate endpoint URL
    if not endpoint.startswith("https://") and not endpoint.startswith("http://"):
        raise ValueError(f"Invalid endpoint URL: {endpoint}. Must start with https:// or http://")

    if "s3" not in endpoint.lower():
        raise ValueError(f"Invalid endpoint URL: {endpoint}. Must contain 's3'")

    return True
