"""Scaleway-specific helpers for naming conventions, tagging, and resource validation."""

import re
from typing import Optional


def validate_bucket_name(name: str) -> bool:
    """
    Validate Scaleway object storage bucket name.

    Bucket names must:
    - Be 3-63 characters long
    - Start and end with lowercase letter or digit
    - Contain only lowercase letters, digits, and hyphens
    - Not be formatted as an IP address

    Args:
        name: Bucket name to validate

    Returns:
        bool: True if valid

    Raises:
        ValueError: If name is invalid
    """
    if not name or len(name) < 3 or len(name) > 63:
        raise ValueError(f"Bucket name must be 3-63 characters, got {len(name)}")

    if not re.match(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$", name):
        raise ValueError(
            f"Bucket name '{name}' must start/end with letter or digit, "
            "contain only lowercase letters, digits, and hyphens"
        )

    if re.match(r"^\d+\.\d+\.\d+\.\d+$", name):
        raise ValueError(f"Bucket name '{name}' cannot be formatted as IP address")

    return True


def validate_database_name(name: str) -> bool:
    """
    Validate Scaleway database name.

    Database names must:
    - Be 1-63 characters long
    - Start with letter
    - Contain only letters, digits, and underscores

    Args:
        name: Database name to validate

    Returns:
        bool: True if valid

    Raises:
        ValueError: If name is invalid
    """
    if not name or len(name) < 1 or len(name) > 63:
        raise ValueError(f"Database name must be 1-63 characters, got {len(name)}")

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name):
        raise ValueError(
            f"Database name '{name}' must start with letter, contain only letters, digits, and underscores"
        )

    return True


def validate_resource_name(name: str, resource_type: str = "resource") -> bool:
    """
    Validate generic Scaleway resource name.

    Args:
        name: Resource name to validate
        resource_type: Type of resource for error messages

    Returns:
        bool: True if valid

    Raises:
        ValueError: If name is invalid
    """
    if not name or len(name) < 1 or len(name) > 255:
        raise ValueError(f"{resource_type} name must be 1-255 characters, got {len(name)}")

    if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9\-_]*[a-zA-Z0-9]$|^[a-zA-Z0-9]$", name):
        raise ValueError(
            f"{resource_type} name '{name}' contains invalid characters. "
            "Use only letters, digits, hyphens, and underscores"
        )

    return True


def format_resource_name(
    base_name: str,
    environment: str,
    suffix: Optional[str] = None,
    separator: str = "-",
) -> str:
    """
    Format a resource name following Scaleway conventions.

    Args:
        base_name: Base name for the resource
        environment: Environment (dev, staging, production)
        suffix: Optional suffix
        separator: Separator character (default: hyphen)

    Returns:
        str: Formatted resource name
    """
    parts = [base_name, environment]
    if suffix:
        parts.append(suffix)

    name = separator.join(parts).lower()
    # Replace underscores with separator
    name = name.replace("_", separator)
    return name


def create_resource_tags(
    environment: str,
    component: str,
    project: str = "evalap",
    additional_tags: Optional[dict[str, str]] = None,
) -> dict[str, str]:
    """
    Create standardized tags for Scaleway resources.

    Args:
        environment: Environment name
        component: Component name
        project: Project name (default: evalap)
        additional_tags: Optional additional tags

    Returns:
        dict: Tags dictionary
    """
    tags = {
        "project": project,
        "environment": environment,
        "component": component,
        "managed-by": "pulumi",
    }

    if additional_tags:
        tags.update(additional_tags)

    return tags


def validate_secret_name(name: str) -> bool:
    """
    Validate Scaleway Secret Manager secret name.

    Secret names must:
    - Be 1-255 characters long
    - Start with lowercase letter
    - Contain only lowercase letters, digits, and hyphens

    Args:
        name: Secret name to validate

    Returns:
        bool: True if valid

    Raises:
        ValueError: If name is invalid
    """
    if not name or len(name) < 1 or len(name) > 255:
        raise ValueError(f"Secret name must be 1-255 characters, got {len(name)}")

    if not re.match(r"^[a-z][a-z0-9-]*$", name):
        raise ValueError(
            f"Secret name '{name}' must start with lowercase letter, "
            "contain only lowercase letters, digits, and hyphens"
        )

    return True


def validate_secret_path(path: str) -> bool:
    """
    Validate Scaleway Secret Manager secret path.

    Secret paths must:
    - Start with /
    - Contain only alphanumeric characters, hyphens, underscores, and slashes

    Args:
        path: Secret path to validate

    Returns:
        bool: True if valid

    Raises:
        ValueError: If path is invalid
    """
    if not path:
        raise ValueError("Secret path cannot be empty")

    if not path.startswith("/"):
        raise ValueError(f"Secret path '{path}' must start with /")

    if not re.match(r"^/[a-zA-Z0-9\-_/]*$", path):
        raise ValueError(
            f"Secret path '{path}' contains invalid characters. "
            "Use only alphanumeric characters, hyphens, underscores, and slashes"
        )

    return True


def validate_cpu_memory_combination(cpu_millicores: int, memory_mb: int) -> bool:
    """
    Validate CPU and memory combination for serverless containers.

    Scaleway has specific CPU/memory combinations:
    - 100m: 128-256 MB
    - 250m: 256-512 MB
    - 500m: 512-1024 MB
    - 1000m: 1024-2048 MB
    - 2000m: 2048-4096 MB
    - 4000m: 4096-8192 MB

    Args:
        cpu_millicores: CPU in millicores
        memory_mb: Memory in MB

    Returns:
        bool: True if valid combination

    Raises:
        ValueError: If combination is invalid
    """
    valid_combinations = {
        100: (128, 256),
        250: (256, 512),
        500: (512, 1024),
        1000: (1024, 2048),
        2000: (2048, 4096),
        4000: (4096, 8192),
    }

    if cpu_millicores not in valid_combinations:
        raise ValueError(
            f"Invalid CPU value {cpu_millicores}m. Valid values: {list(valid_combinations.keys())}"
        )

    min_mem, max_mem = valid_combinations[cpu_millicores]
    if not (min_mem <= memory_mb <= max_mem):
        raise ValueError(f"For CPU {cpu_millicores}m, memory must be {min_mem}-{max_mem}MB, got {memory_mb}MB")

    return True
