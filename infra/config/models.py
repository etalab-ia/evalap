"""Pydantic configuration models for infrastructure components."""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ContainerConfig(BaseModel):
    """Configuration for serverless container deployment."""

    cpu: int = Field(
        default=1000,
        ge=100,
        le=4000,
        description="CPU allocation in millicores (100-4000)",
    )
    memory: int = Field(
        default=1024,
        ge=128,
        le=8192,
        description="Memory allocation in MB (128-8192)",
    )
    max_concurrency: int = Field(default=80, ge=1, le=80, description="Maximum concurrent requests (max 80)")
    timeout: int = Field(default=300, ge=10, le=3600, description="Request timeout in seconds")
    port: int = Field(default=8080, ge=1, le=65535, description="Container listening port (1-65535)")
    environment_variables: dict[str, str] = Field(
        default_factory=dict, description="Environment variables for container"
    )
    secret_environment_variables: dict[str, str] = Field(
        default_factory=dict,
        description="Secret environment variables (stored securely, not displayed after validation)",
    )

    @field_validator("memory")
    @classmethod
    def validate_memory_cpu_ratio(cls, v, info):
        """Ensure memory is appropriate for CPU allocation."""
        if "cpu" in info.data:
            cpu = info.data["cpu"]
            min_memory = cpu // 4
            max_memory = cpu * 8
            if not (min_memory <= v <= max_memory):
                raise ValueError(
                    f"Memory {v}MB must be between {min_memory}MB and {max_memory}MB for CPU {cpu}m"
                )
        return v


class DatabaseConfig(BaseModel):
    """Configuration for managed PostgreSQL database."""

    engine: str = Field(default="PostgreSQL-15", description="Database engine version")
    volume_size: int = Field(
        default=20,
        ge=5,
        le=500,
        description="Volume size in GB (5-500)",
    )
    backup_retention_days: int = Field(
        default=7,
        ge=1,
        le=365,
        description="Backup retention in days (1-365)",
    )
    enable_backups: bool = Field(default=True, description="Enable automated backups")
    enable_high_availability: bool = Field(default=False, description="Enable high availability mode")
    user_name: str = Field(default="postgres", description="Database admin username")
    database_name: str = Field(default="evalap", description="Default database name")


class StorageConfig(BaseModel):
    """Configuration for object storage bucket."""

    versioning_enabled: bool = Field(default=True, description="Enable object versioning")
    lifecycle_expiration_days: Optional[int] = Field(
        default=None, description="Auto-delete objects after N days"
    )
    acl: str = Field(default="private", description="Access control level")
    encryption_enabled: bool = Field(default=True, description="Enable encryption")


class NetworkConfig(BaseModel):
    """Configuration for private networking."""

    enable_private_network: bool = Field(default=False, description="Enable private network isolation")
    cidr_block: str = Field(default="10.0.0.0/16", description="CIDR block for private network")
    enable_nat_gateway: bool = Field(default=False, description="Enable NAT gateway for outbound traffic")


class SecretConfig(BaseModel):
    """Configuration for a secret in Scaleway Secret Manager."""

    name: str = Field(description="Secret name (must match ^[a-z][a-z0-9-]*$)")
    description: Optional[str] = Field(default=None, description="Human-readable description")
    data: str = Field(description="Secret data/value to store")
    path: str = Field(default="/", description="Secret path in Secret Manager")
    secret_type: Optional[str] = Field(
        default=None,
        description="Secret type (opaque, certificate, key_value, basic_credentials, etc.)",
    )
    protected: bool = Field(default=False, description="Protect secret from deletion")

    @field_validator("name")
    @classmethod
    def validate_secret_name(cls, v):
        """Ensure secret name follows Scaleway naming convention."""
        import re

        if not re.match(r"^[a-z][a-z0-9-]*$", v):
            raise ValueError(f"Secret name '{v}' must match pattern ^[a-z][a-z0-9-]*$")
        if len(v) > 255:
            raise ValueError(f"Secret name must be <= 255 characters, got {len(v)}")
        return v


class MonitoringConfig(BaseModel):
    """Configuration for monitoring and observability."""

    enable_cockpit: bool = Field(default=True, description="Enable Cockpit monitoring")
    metrics_retention_days: int = Field(default=30, ge=1, le=365, description="Metrics retention period")
    log_retention_days: int = Field(default=30, ge=1, le=365, description="Log retention period")
    enable_alerts: bool = Field(default=True, description="Enable alert rules")
    alert_email: Optional[str] = Field(default=None, description="Email for alerts")


class IAMRuleConfig(BaseModel):
    """Configuration for a single IAM policy rule."""

    service: str = Field(
        description="Service type: serverless_containers, database, object_storage, "
        "secret_manager, container_registry, cockpit, vpc"
    )
    access_level: str = Field(description="Access level (full_access, read_only, etc.)")
    project_ids: Optional[list[str]] = Field(
        default=None,
        description="List of project IDs to scope the rule (mutually exclusive with organization_id)",
    )
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID to scope the rule (mutually exclusive with project_ids)",
    )

    @field_validator("service")
    @classmethod
    def validate_service(cls, v):
        """Ensure service is one of the allowed values."""
        allowed = {
            "serverless_containers",
            "database",
            "object_storage",
            "secret_manager",
            "container_registry",
            "cockpit",
            "vpc",
        }
        if v not in allowed:
            raise ValueError(f"Service must be one of {allowed}")
        return v


class IAMPolicyConfig(BaseModel):
    """Configuration for an IAM policy with multiple rules."""

    name: str = Field(description="Policy name")
    description: str = Field(description="Human-readable description of the policy purpose")
    rules: list[IAMRuleConfig] = Field(description="List of policy rules")
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID for the IAM application",
    )
    create_api_key: bool = Field(
        default=False,
        description="Whether to create an API key for the application",
    )


class StackConfiguration(BaseModel):
    """Complete stack configuration combining all components."""

    stack_name: str = Field(description="Name of the Pulumi stack")
    environment: str = Field(description="Environment name (dev, staging, production)")
    region: str = Field(default="fr-par", description="Scaleway region")
    project_id: str = Field(description="Scaleway project ID")
    container: ContainerConfig = Field(default_factory=ContainerConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    network: NetworkConfig = Field(default_factory=NetworkConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    iam_policies: list[IAMPolicyConfig] = Field(default_factory=list, description="IAM policies to create")
    tags: dict[str, str] = Field(default_factory=dict, description="Common tags for all resources")

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v):
        """Ensure environment is one of the allowed values."""
        allowed = {"dev", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v
