"""IAM Policy component for Scaleway IAM with least privilege principle."""

import logging
from enum import Enum
from typing import Any, Optional

import pulumi
import pulumiverse_scaleway as scaleway

from infra.components import BaseComponent
from infra.utils import pulumi_helpers, scaleway_helpers

logger = logging.getLogger(__name__)


class ServiceType(str, Enum):
    """Service types for predefined permission sets."""

    SERVERLESS_CONTAINERS = "serverless_containers"
    DATABASE = "database"
    OBJECT_STORAGE = "object_storage"
    SECRET_MANAGER = "secret_manager"
    CONTAINER_REGISTRY = "container_registry"
    COCKPIT = "cockpit"
    VPC = "vpc"


# Predefined permission sets for least privilege access
# Reference: https://www.scaleway.com/en/docs/iam/reference-content/permission-sets/
PERMISSION_SETS = {
    ServiceType.SERVERLESS_CONTAINERS: {
        "full_access": ["ContainersFullAccess"],
        "read_only": ["ContainersReadOnly"],
        "deploy_only": ["ContainersNamespacesCreate", "ContainersNamespacesDelete"],
    },
    ServiceType.DATABASE: {
        "full_access": ["RelationalDatabasesFullAccess"],
        "read_only": ["RelationalDatabasesReadOnly"],
    },
    ServiceType.OBJECT_STORAGE: {
        "full_access": ["ObjectStorageFullAccess"],
        "read_only": ["ObjectStorageReadOnly"],
        "write_only": ["ObjectStorageObjectsWrite", "ObjectStorageBucketsWrite"],
    },
    ServiceType.SECRET_MANAGER: {
        "full_access": ["SecretManagerFullAccess"],
        "read_only": ["SecretManagerReadOnly"],
        "secret_access": ["SecretManagerSecretAccess"],
    },
    ServiceType.CONTAINER_REGISTRY: {
        "full_access": ["ContainerRegistryFullAccess"],
        "read_only": ["ContainerRegistryReadOnly"],
    },
    ServiceType.COCKPIT: {
        "full_access": ["ObservabilityFullAccess"],
        "read_only": ["ObservabilityReadOnly"],
        "logs_only": ["ObservabilityLogsRead"],
        "metrics_only": ["ObservabilityMetricsRead"],
    },
    ServiceType.VPC: {
        "full_access": ["VPCFullAccess"],
        "read_only": ["VPCReadOnly"],
    },
}


class IAMPolicyConfig:
    """Configuration for an IAM policy rule."""

    def __init__(
        self,
        service: ServiceType,
        access_level: str,
        project_ids: Optional[list[str]] = None,
        organization_id: Optional[str] = None,
    ):
        """
        Initialize IAM policy rule configuration.

        Args:
            service: Service type for permission set
            access_level: Access level (full_access, read_only, etc.)
            project_ids: List of project IDs to scope the rule (mutually exclusive with organization_id)
            organization_id: Organization ID to scope the rule (mutually exclusive with project_ids)

        Raises:
            ValueError: If access_level is not valid for the service
        """
        if service not in PERMISSION_SETS:
            raise ValueError(f"Unknown service type: {service}")

        if access_level not in PERMISSION_SETS[service]:
            valid_levels = list(PERMISSION_SETS[service].keys())
            raise ValueError(
                f"Invalid access level '{access_level}' for {service}. Valid levels: {valid_levels}"
            )

        if project_ids and organization_id:
            raise ValueError("Cannot specify both project_ids and organization_id")

        if not project_ids and not organization_id:
            raise ValueError("Must specify either project_ids or organization_id")

        self.service = service
        self.access_level = access_level
        self.project_ids = project_ids
        self.organization_id = organization_id

    @property
    def permission_set_names(self) -> list[str]:
        """Get the permission set names for this configuration."""
        return PERMISSION_SETS[self.service][self.access_level]


class IAMPolicy(BaseComponent):
    """
    IAM Policy component for Scaleway IAM.

    Creates IAM applications and policies with service-specific role definitions
    following the principle of least privilege.
    """

    def __init__(
        self,
        name: str,
        environment: str,
        description: str,
        rules: list[IAMPolicyConfig],
        organization_id: Optional[str] = None,
        tags: Optional[dict[str, str]] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """
        Initialize IAM Policy component.

        Args:
            name: Component name (used for application and policy naming)
            environment: Environment (dev, staging, production)
            description: Human-readable description of the policy purpose
            rules: List of IAMPolicyConfig rules defining permissions
            organization_id: Optional organization ID for the application
            tags: Optional tags for resources
            opts: Optional Pulumi resource options
        """
        super().__init__(name, environment, tags, opts)
        self.description = description
        self.rules = rules
        self.organization_id = organization_id

        # Initialize resource references
        self.application: Optional[scaleway.iam.Application] = None
        self.policy: Optional[scaleway.iam.Policy] = None
        self.api_key: Optional[scaleway.iam.ApiKey] = None

    def create(self) -> None:
        """Create IAM application and policy with configured rules."""
        try:
            pulumi_helpers.log_resource_creation(
                "IAMPolicy",
                self.name,
                environment=self.environment,
                rule_count=len(self.rules),
            )

            # Create IAM application
            self._create_application()

            # Create IAM policy with rules
            self._create_policy()

            logger.info(f"IAMPolicy '{self.name}' created with {len(self.rules)} rules")
        except Exception as e:
            pulumi_helpers.handle_error(e, f"IAMPolicy.create({self.name})")

    def _create_application(self) -> None:
        """Create the IAM application."""
        app_name = scaleway_helpers.format_resource_name(self.name, self.environment)

        logger.debug(f"Creating IAM application: {app_name}")

        app_args = {
            "name": app_name,
            "description": self.description,
            "tags": self._format_tags_list(),
        }

        if self.organization_id:
            app_args["organization_id"] = self.organization_id

        self.application = scaleway.iam.Application(
            f"{self.name}-app",
            **app_args,
            opts=self.opts,
        )

        logger.debug(f"Created IAM application: {app_name}")

    def _create_policy(self) -> None:
        """Create the IAM policy with configured rules."""
        policy_name = scaleway_helpers.format_resource_name(f"{self.name}-policy", self.environment)

        logger.debug(f"Creating IAM policy: {policy_name}")

        # Build policy rules
        policy_rules = []
        for rule_config in self.rules:
            rule_args = {
                "permission_set_names": rule_config.permission_set_names,
            }

            if rule_config.project_ids:
                rule_args["project_ids"] = rule_config.project_ids
            elif rule_config.organization_id:
                rule_args["organization_id"] = rule_config.organization_id

            policy_rules.append(rule_args)

        # Create policy with application as principal
        policy_opts = pulumi.ResourceOptions(parent=self.application) if self.opts else None

        policy_args = {
            "name": policy_name,
            "description": self.description,
            "application_id": self.application.id,
            "rules": policy_rules,
            "tags": self._format_tags_list(),
        }

        if self.organization_id:
            policy_args["organization_id"] = self.organization_id

        self.policy = scaleway.iam.Policy(
            f"{self.name}-policy",
            **policy_args,
            opts=policy_opts,
        )

        logger.debug(f"Created IAM policy: {policy_name}")

    def create_api_key(self, description: Optional[str] = None) -> pulumi.Output:
        """
        Create an API key for the IAM application.

        Args:
            description: Optional description for the API key

        Returns:
            pulumi.Output: API key secret key (sensitive)

        Raises:
            RuntimeError: If application has not been created
        """
        if not self.application:
            raise RuntimeError("Application must be created before creating API key")

        key_description = description or f"API key for {self.name} ({self.environment})"

        api_key_opts = pulumi.ResourceOptions(parent=self.application) if self.opts else None

        self.api_key = scaleway.iam.ApiKey(
            f"{self.name}-api-key",
            application_id=self.application.id,
            description=key_description,
            opts=api_key_opts,
        )

        logger.info(f"Created API key for application '{self.name}'")
        return self.api_key.secret_key

        """
        Format tags as a list of strings for Scaleway IAM.

        Uses "=" as separator and deduplicates tags.

        Returns:
            list[str]: Tags as list of strings
        """
        # Start with default tags
        final_tags = {
            "environment": self.environment,
            "component": self.name,
            "managed-by": "pulumi",
        }

        # Merge custom tags (overwriting defaults if keys match)
        if self.tags:
            for key, value in self.tags.items():
                final_tags[key] = str(value)

        # Format as key=value list
        return [f"{key}={value}" for key, value in final_tags.items()]

    def get_outputs(self) -> dict[str, Any]:
        """
        Get component outputs.

        Returns:
            dict: Dictionary containing:
                - application_id: IAM application ID
                - policy_id: IAM policy ID
                - api_key_access_key: API key access key (if created)
                - rule_count: Number of policy rules
        """
        outputs = {
            "application_id": self.application.id if self.application else None,
            "policy_id": self.policy.id if self.policy else None,
            "rule_count": len(self.rules),
        }

        if self.api_key:
            outputs["api_key_access_key"] = self.api_key.access_key

        return outputs

    def get_application_id(self) -> pulumi.Output:
        """
        Get the IAM application ID.

        Returns:
            pulumi.Output: Application ID

        Raises:
            RuntimeError: If application has not been created
        """
        if not self.application:
            raise RuntimeError("Application has not been created")
        return self.application.id

    def get_policy_id(self) -> pulumi.Output:
        """
        Get the IAM policy ID.

        Returns:
            pulumi.Output: Policy ID

        Raises:
            RuntimeError: If policy has not been created
        """
        if not self.policy:
            raise RuntimeError("Policy has not been created")
        return self.policy.id


def create_service_policy(
    name: str,
    environment: str,
    service: ServiceType,
    access_level: str,
    project_id: str,
    description: Optional[str] = None,
    tags: Optional[dict[str, str]] = None,
    opts: Optional[pulumi.ResourceOptions] = None,
) -> IAMPolicy:
    """
    Create a simple IAM policy for a single service.

    This is a convenience function for creating policies with a single rule.

    Args:
        name: Policy name
        environment: Environment (dev, staging, production)
        service: Service type
        access_level: Access level for the service
        project_id: Project ID to scope the policy
        description: Optional description
        tags: Optional tags
        opts: Optional Pulumi resource options

    Returns:
        IAMPolicy: Configured IAM policy component
    """
    rule = IAMPolicyConfig(
        service=service,
        access_level=access_level,
        project_ids=[project_id],
    )

    policy_description = description or f"{service.value} {access_level} access for {name}"

    policy = IAMPolicy(
        name=name,
        environment=environment,
        description=policy_description,
        rules=[rule],
        tags=tags,
        opts=opts,
    )

    return policy


def create_evalap_service_policy(
    environment: str,
    project_id: str,
    tags: Optional[dict[str, str]] = None,
    opts: Optional[pulumi.ResourceOptions] = None,
) -> IAMPolicy:
    """
    Create the standard EvalAP service policy with least privilege.

    This creates a policy with the minimum permissions needed for EvalAP:
    - Serverless Containers: full access (deploy and manage containers)
    - Database: full access (manage PostgreSQL)
    - Object Storage: full access (store artifacts)
    - Secret Manager: secret access only (read secrets, not manage)
    - Container Registry: read only (pull images)
    - Cockpit: read only (view metrics and logs)

    Args:
        environment: Environment (dev, staging, production)
        project_id: Project ID to scope the policy
        tags: Optional tags
        opts: Optional Pulumi resource options

    Returns:
        IAMPolicy: Configured IAM policy for EvalAP
    """
    rules = [
        IAMPolicyConfig(
            service=ServiceType.SERVERLESS_CONTAINERS,
            access_level="full_access",
            project_ids=[project_id],
        ),
        IAMPolicyConfig(
            service=ServiceType.DATABASE,
            access_level="full_access",
            project_ids=[project_id],
        ),
        IAMPolicyConfig(
            service=ServiceType.OBJECT_STORAGE,
            access_level="full_access",
            project_ids=[project_id],
        ),
        IAMPolicyConfig(
            service=ServiceType.SECRET_MANAGER,
            access_level="secret_access",
            project_ids=[project_id],
        ),
        IAMPolicyConfig(
            service=ServiceType.CONTAINER_REGISTRY,
            access_level="read_only",
            project_ids=[project_id],
        ),
        IAMPolicyConfig(
            service=ServiceType.COCKPIT,
            access_level="read_only",
            project_ids=[project_id],
        ),
    ]

    policy = IAMPolicy(
        name="evalap-service",
        environment=environment,
        description="EvalAP service account with least privilege access",
        rules=rules,
        tags=tags,
        opts=opts,
    )

    return policy


def create_ci_cd_policy(
    environment: str,
    project_id: str,
    tags: Optional[dict[str, str]] = None,
    opts: Optional[pulumi.ResourceOptions] = None,
) -> IAMPolicy:
    """
    Create a CI/CD pipeline policy with deployment permissions.

    This creates a policy for CI/CD pipelines with permissions to:
    - Deploy serverless containers
    - Push to container registry
    - Read secrets for deployment
    - Read monitoring data

    Args:
        environment: Environment (dev, staging, production)
        project_id: Project ID to scope the policy
        tags: Optional tags
        opts: Optional Pulumi resource options

    Returns:
        IAMPolicy: Configured IAM policy for CI/CD
    """
    rules = [
        IAMPolicyConfig(
            service=ServiceType.SERVERLESS_CONTAINERS,
            access_level="full_access",
            project_ids=[project_id],
        ),
        IAMPolicyConfig(
            service=ServiceType.CONTAINER_REGISTRY,
            access_level="full_access",
            project_ids=[project_id],
        ),
        IAMPolicyConfig(
            service=ServiceType.SECRET_MANAGER,
            access_level="read_only",
            project_ids=[project_id],
        ),
        IAMPolicyConfig(
            service=ServiceType.COCKPIT,
            access_level="read_only",
            project_ids=[project_id],
        ),
    ]

    policy = IAMPolicy(
        name="evalap-cicd",
        environment=environment,
        description="CI/CD pipeline with deployment permissions",
        rules=rules,
        tags=tags,
        opts=opts,
    )

    return policy


def create_readonly_policy(
    name: str,
    environment: str,
    project_id: str,
    services: Optional[list[ServiceType]] = None,
    tags: Optional[dict[str, str]] = None,
    opts: Optional[pulumi.ResourceOptions] = None,
) -> IAMPolicy:
    """
    Create a read-only policy for specified services.

    Args:
        name: Policy name
        environment: Environment (dev, staging, production)
        project_id: Project ID to scope the policy
        services: List of services to grant read access (defaults to all)
        tags: Optional tags
        opts: Optional Pulumi resource options

    Returns:
        IAMPolicy: Configured read-only IAM policy
    """
    if services is None:
        services = list(ServiceType)

    rules = []
    for service in services:
        if "read_only" in PERMISSION_SETS[service]:
            rules.append(
                IAMPolicyConfig(
                    service=service,
                    access_level="read_only",
                    project_ids=[project_id],
                )
            )

    policy = IAMPolicy(
        name=name,
        environment=environment,
        description=f"Read-only access to {len(rules)} services",
        rules=rules,
        tags=tags,
        opts=opts,
    )

    return policy
