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


def validate_private_network_cidr(cidr: str) -> bool:
    """
    Validate CIDR block is a valid private network range.

    Private network ranges (RFC 1918):
    - 10.0.0.0/8 (10.0.0.0 - 10.255.255.255)
    - 172.16.0.0/12 (172.16.0.0 - 172.31.255.255)
    - 192.168.0.0/16 (192.168.0.0 - 192.168.255.255)

    Args:
        cidr: CIDR block string (e.g., 10.0.0.0/16)

    Returns:
        bool: True if valid private network range

    Raises:
        ValueError: If CIDR is not a valid private network range
    """
    # First validate basic CIDR format
    validate_cidr_block(cidr)

    ip_part = cidr.split("/")[0]
    octets = [int(o) for o in ip_part.split(".")]

    # Check if in 10.0.0.0/8 range
    if octets[0] == 10:
        return True

    # Check if in 172.16.0.0/12 range (172.16.x.x - 172.31.x.x)
    if octets[0] == 172 and 16 <= octets[1] <= 31:
        return True

    # Check if in 192.168.0.0/16 range
    if octets[0] == 192 and octets[1] == 168:
        return True

    raise ValueError(
        f"CIDR '{cidr}' is not a valid private network range. "
        "Must be within 10.0.0.0/8, 172.16.0.0/12, or 192.168.0.0/16"
    )


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
    Validate IAM policy structure (legacy AWS-style format).

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


# Scaleway IAM permission sets by service
# Reference: https://www.scaleway.com/en/docs/iam/reference-content/permission-sets/
SCALEWAY_PERMISSION_SETS = {
    "serverless_containers": {
        "full_access": ["ContainersFullAccess"],
        "read_only": ["ContainersReadOnly"],
        "deploy_only": ["ContainersNamespacesCreate", "ContainersNamespacesDelete"],
    },
    "database": {
        "full_access": ["RelationalDatabasesFullAccess"],
        "read_only": ["RelationalDatabasesReadOnly"],
    },
    "object_storage": {
        "full_access": ["ObjectStorageFullAccess"],
        "read_only": ["ObjectStorageReadOnly"],
        "write_only": ["ObjectStorageObjectsWrite", "ObjectStorageBucketsWrite"],
    },
    "secret_manager": {
        "full_access": ["SecretManagerFullAccess"],
        "read_only": ["SecretManagerReadOnly"],
        "secret_access": ["SecretManagerSecretAccess"],
    },
    "container_registry": {
        "full_access": ["ContainerRegistryFullAccess"],
        "read_only": ["ContainerRegistryReadOnly"],
    },
    "cockpit": {
        "full_access": ["ObservabilityFullAccess"],
        "read_only": ["ObservabilityReadOnly"],
        "logs_only": ["ObservabilityLogsRead"],
        "metrics_only": ["ObservabilityMetricsRead"],
    },
    "vpc": {
        "full_access": ["VPCFullAccess"],
        "read_only": ["VPCReadOnly"],
    },
}


def validate_iam_rule_config(rule: Any) -> bool:
    """
    Validate Scaleway IAM rule configuration.

    Args:
        rule: IAMRuleConfig object to validate

    Returns:
        bool: True if valid

    Raises:
        ValueError: If rule is invalid
    """
    # Validate service type
    if rule.service not in SCALEWAY_PERMISSION_SETS:
        valid_services = list(SCALEWAY_PERMISSION_SETS.keys())
        raise ValueError(f"Invalid service '{rule.service}'. Must be one of: {valid_services}")

    # Validate access level for service
    valid_levels = list(SCALEWAY_PERMISSION_SETS[rule.service].keys())
    if rule.access_level not in valid_levels:
        raise ValueError(
            f"Invalid access level '{rule.access_level}' for service '{rule.service}'. "
            f"Must be one of: {valid_levels}"
        )

    # Validate scope (must have either project_ids or organization_id, not both)
    if rule.project_ids and rule.organization_id:
        raise ValueError("Cannot specify both project_ids and organization_id in a rule")

    if not rule.project_ids and not rule.organization_id:
        raise ValueError("Must specify either project_ids or organization_id in a rule")

    # Validate project_ids format if provided
    if rule.project_ids:
        for project_id in rule.project_ids:
            if not validate_uuid(project_id):
                raise ValueError(f"Invalid project ID format: {project_id}")

    # Validate organization_id format if provided
    if rule.organization_id:
        if not validate_uuid(rule.organization_id):
            raise ValueError(f"Invalid organization ID format: {rule.organization_id}")

    return True


def validate_iam_policy_config(config: Any) -> bool:
    """
    Validate Scaleway IAM policy configuration.

    Args:
        config: IAMPolicyConfig object to validate

    Returns:
        bool: True if valid

    Raises:
        ValueError: If configuration is invalid
    """
    # Validate policy name
    if not config.name:
        raise ValueError("Policy name cannot be empty")

    if len(config.name) > 64:
        raise ValueError(f"Policy name must be <= 64 characters, got {len(config.name)}")

    # Validate description
    if not config.description:
        raise ValueError("Policy description cannot be empty")

    # Validate rules
    if not config.rules:
        raise ValueError("Policy must have at least one rule")

    for rule in config.rules:
        validate_iam_rule_config(rule)

    return True


def validate_uuid(value: str) -> bool:
    """
    Validate UUID format.

    Args:
        value: String to validate

    Returns:
        bool: True if valid UUID format
    """
    uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    return bool(re.match(uuid_pattern, value.lower()))


def validate_least_privilege(rules: list[Any], required_services: list[str]) -> bool:
    """
    Validate that IAM rules follow least privilege principle.

    Checks that:
    1. Only required services have permissions
    2. No unnecessary full_access when read_only would suffice
    3. All rules are scoped to specific projects (not organization-wide)

    Args:
        rules: List of IAMRuleConfig objects
        required_services: List of services that need access

    Returns:
        bool: True if valid

    Raises:
        ValueError: If rules violate least privilege principle
    """
    rule_services = {rule.service for rule in rules}

    # Check for unnecessary services
    unnecessary = rule_services - set(required_services)
    if unnecessary:
        raise ValueError(f"Least privilege violation: unnecessary services granted access: {unnecessary}")

    # Check for organization-wide access (should be project-scoped)
    for rule in rules:
        if rule.organization_id:
            raise ValueError(
                f"Least privilege violation: service '{rule.service}' has organization-wide access. "
                "Use project_ids for more restrictive access."
            )

    return True


def validate_secret_name(name: str) -> bool:
    """
    Validate secret name.

    Args:
        name: Secret name

    Returns:
        bool: True if valid

    Raises:
        ValueError: If name is invalid
    """
    return scaleway_helpers.validate_secret_name(name)


def validate_secret_path(path: str) -> bool:
    """
    Validate secret path.

    Args:
        path: Secret path

    Returns:
        bool: True if valid

    Raises:
        ValueError: If path is invalid
    """
    return scaleway_helpers.validate_secret_path(path)


def validate_secret_config(config: Any) -> bool:
    """
    Validate secret configuration.

    Args:
        config: SecretConfig object to validate

    Returns:
        bool: True if valid

    Raises:
        ValueError: If configuration is invalid
    """
    # Validate secret name
    validate_secret_name(config.name)

    # Validate secret path
    validate_secret_path(config.path)

    # Validate secret data is not empty
    if not config.data:
        raise ValueError("Secret data cannot be empty")

    # Validate secret type if provided
    valid_types = [
        None,
        "opaque",
        "certificate",
        "key_value",
        "basic_credentials",
        "database_credentials",
        "ssh_key",
    ]
    if config.secret_type not in valid_types:
        raise ValueError(
            f"Invalid secret type '{config.secret_type}'. Must be one of: {[t for t in valid_types if t]}"
        )

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
