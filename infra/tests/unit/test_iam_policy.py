"""Unit tests for IAMPolicy component."""

from unittest.mock import MagicMock, patch

import pytest

from infra.components.iam_policy import (
    PERMISSION_SETS,
    IAMPolicy,
    IAMPolicyConfig,
    ServiceType,
    create_ci_cd_policy,
    create_evalap_service_policy,
    create_readonly_policy,
    create_service_policy,
)
from infra.config.models import IAMPolicyConfig as IAMPolicyConfigModel
from infra.config.models import IAMRuleConfig
from infra.utils.validation import (
    SCALEWAY_PERMISSION_SETS,
    validate_iam_policy_config,
    validate_iam_rule_config,
    validate_least_privilege,
    validate_uuid,
)


class TestServiceType:
    """Tests for ServiceType enum."""

    def test_all_service_types_have_permission_sets(self):
        """Test that all service types have defined permission sets."""
        for service_type in ServiceType:
            assert service_type in PERMISSION_SETS
            assert len(PERMISSION_SETS[service_type]) > 0

    def test_service_type_values(self):
        """Test service type string values."""
        assert ServiceType.SERVERLESS_CONTAINERS.value == "serverless_containers"
        assert ServiceType.DATABASE.value == "database"
        assert ServiceType.OBJECT_STORAGE.value == "object_storage"
        assert ServiceType.SECRET_MANAGER.value == "secret_manager"
        assert ServiceType.CONTAINER_REGISTRY.value == "container_registry"
        assert ServiceType.COCKPIT.value == "cockpit"
        assert ServiceType.VPC.value == "vpc"


class TestPermissionSets:
    """Tests for permission set definitions."""

    def test_serverless_containers_permission_sets(self):
        """Test serverless containers permission sets."""
        perms = PERMISSION_SETS[ServiceType.SERVERLESS_CONTAINERS]
        assert "full_access" in perms
        assert "read_only" in perms
        assert "ContainersFullAccess" in perms["full_access"]
        assert "ContainersReadOnly" in perms["read_only"]

    def test_database_permission_sets(self):
        """Test database permission sets."""
        perms = PERMISSION_SETS[ServiceType.DATABASE]
        assert "full_access" in perms
        assert "read_only" in perms
        assert "RelationalDatabasesFullAccess" in perms["full_access"]

    def test_object_storage_permission_sets(self):
        """Test object storage permission sets."""
        perms = PERMISSION_SETS[ServiceType.OBJECT_STORAGE]
        assert "full_access" in perms
        assert "read_only" in perms
        assert "write_only" in perms
        assert "ObjectStorageFullAccess" in perms["full_access"]

    def test_secret_manager_permission_sets(self):
        """Test secret manager permission sets."""
        perms = PERMISSION_SETS[ServiceType.SECRET_MANAGER]
        assert "full_access" in perms
        assert "read_only" in perms
        assert "secret_access" in perms
        assert "SecretManagerSecretAccess" in perms["secret_access"]

    def test_cockpit_permission_sets(self):
        """Test cockpit permission sets."""
        perms = PERMISSION_SETS[ServiceType.COCKPIT]
        assert "full_access" in perms
        assert "read_only" in perms
        assert "logs_only" in perms
        assert "metrics_only" in perms


class TestIAMPolicyConfig:
    """Tests for IAMPolicyConfig class."""

    def test_valid_config_with_project_ids(self):
        """Test valid configuration with project IDs."""
        config = IAMPolicyConfig(
            service=ServiceType.DATABASE,
            access_level="full_access",
            project_ids=["project-123"],
        )
        assert config.service == ServiceType.DATABASE
        assert config.access_level == "full_access"
        assert config.project_ids == ["project-123"]
        assert config.organization_id is None

    def test_valid_config_with_organization_id(self):
        """Test valid configuration with organization ID."""
        config = IAMPolicyConfig(
            service=ServiceType.OBJECT_STORAGE,
            access_level="read_only",
            organization_id="org-456",
        )
        assert config.organization_id == "org-456"
        assert config.project_ids is None

    def test_permission_set_names_property(self):
        """Test that permission_set_names returns correct values."""
        config = IAMPolicyConfig(
            service=ServiceType.SECRET_MANAGER,
            access_level="secret_access",
            project_ids=["project-123"],
        )
        assert config.permission_set_names == ["SecretManagerSecretAccess"]

    def test_invalid_service_type(self):
        """Test that invalid service type raises error."""
        with pytest.raises(ValueError) as exc_info:
            IAMPolicyConfig(
                service="invalid_service",
                access_level="full_access",
                project_ids=["project-123"],
            )
        assert "Unknown service type" in str(exc_info.value)

    def test_invalid_access_level(self):
        """Test that invalid access level raises error."""
        with pytest.raises(ValueError) as exc_info:
            IAMPolicyConfig(
                service=ServiceType.DATABASE,
                access_level="invalid_level",
                project_ids=["project-123"],
            )
        assert "Invalid access level" in str(exc_info.value)

    def test_both_project_and_org_raises_error(self):
        """Test that specifying both project_ids and organization_id raises error."""
        with pytest.raises(ValueError) as exc_info:
            IAMPolicyConfig(
                service=ServiceType.DATABASE,
                access_level="full_access",
                project_ids=["project-123"],
                organization_id="org-456",
            )
        assert "Cannot specify both" in str(exc_info.value)

    def test_neither_project_nor_org_raises_error(self):
        """Test that specifying neither project_ids nor organization_id raises error."""
        with pytest.raises(ValueError) as exc_info:
            IAMPolicyConfig(
                service=ServiceType.DATABASE,
                access_level="full_access",
            )
        assert "Must specify either" in str(exc_info.value)


class TestIAMPolicy:
    """Tests for IAMPolicy component."""

    @pytest.fixture
    def sample_rules(self):
        """Create sample IAM policy rules."""
        return [
            IAMPolicyConfig(
                service=ServiceType.SERVERLESS_CONTAINERS,
                access_level="full_access",
                project_ids=["project-123"],
            ),
            IAMPolicyConfig(
                service=ServiceType.DATABASE,
                access_level="read_only",
                project_ids=["project-123"],
            ),
        ]

    @pytest.fixture
    def iam_policy(self, sample_rules):
        """Create an IAMPolicy instance for testing."""
        return IAMPolicy(
            name="test-policy",
            environment="dev",
            description="Test IAM policy",
            rules=sample_rules,
            tags={"team": "platform"},
        )

    def test_iam_policy_initialization(self, iam_policy, sample_rules):
        """Test that IAMPolicy initializes correctly."""
        assert iam_policy.name == "test-policy"
        assert iam_policy.environment == "dev"
        assert iam_policy.description == "Test IAM policy"
        assert len(iam_policy.rules) == 2
        assert iam_policy.tags == {"team": "platform"}
        assert iam_policy.application is None
        assert iam_policy.policy is None
        assert iam_policy.api_key is None

    def test_format_tags_list(self, iam_policy):
        """Test tag formatting."""
        tags = iam_policy._format_tags_list()
        assert "environment:dev" in tags
        assert "component:test-policy" in tags
        assert "managed-by:pulumi" in tags
        assert "team:platform" in tags

    def test_get_outputs_before_create(self, iam_policy):
        """Test get_outputs before resources are created."""
        outputs = iam_policy.get_outputs()
        assert outputs["application_id"] is None
        assert outputs["policy_id"] is None
        assert outputs["rule_count"] == 2

    def test_get_application_id_before_create_raises(self, iam_policy):
        """Test that get_application_id raises error before create."""
        with pytest.raises(RuntimeError) as exc_info:
            iam_policy.get_application_id()
        assert "has not been created" in str(exc_info.value)

    def test_get_policy_id_before_create_raises(self, iam_policy):
        """Test that get_policy_id raises error before create."""
        with pytest.raises(RuntimeError) as exc_info:
            iam_policy.get_policy_id()
        assert "has not been created" in str(exc_info.value)

    def test_create_api_key_before_create_raises(self, iam_policy):
        """Test that create_api_key raises error before application is created."""
        with pytest.raises(RuntimeError) as exc_info:
            iam_policy.create_api_key()
        assert "must be created before" in str(exc_info.value)

    @patch("infra.components.iam_policy.scaleway")
    @patch("infra.components.iam_policy.pulumi_helpers")
    @patch("infra.components.iam_policy.scaleway_helpers")
    def test_create_calls_scaleway(
        self, mock_scaleway_helpers, mock_pulumi_helpers, mock_scaleway, iam_policy
    ):
        """Test that create() calls Scaleway IAM resources."""
        mock_scaleway_helpers.format_resource_name.return_value = "test-policy-dev"

        # Mock IAM Application
        mock_app = MagicMock()
        mock_app.id = "app-id-123"
        mock_scaleway.iam.Application.return_value = mock_app

        # Mock IAM Policy
        mock_policy = MagicMock()
        mock_policy.id = "policy-id-456"
        mock_scaleway.iam.Policy.return_value = mock_policy

        iam_policy.create()

        # Verify Application was created
        mock_scaleway.iam.Application.assert_called_once()
        call_args = mock_scaleway.iam.Application.call_args
        assert call_args[0][0] == "test-policy-app"

        # Verify Policy was created
        mock_scaleway.iam.Policy.assert_called_once()
        policy_call_args = mock_scaleway.iam.Policy.call_args
        assert policy_call_args[0][0] == "test-policy-policy"

        # Verify resources are stored
        assert iam_policy.application == mock_app
        assert iam_policy.policy == mock_policy


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_create_service_policy(self):
        """Test create_service_policy function."""
        policy = create_service_policy(
            name="db-access",
            environment="staging",
            service=ServiceType.DATABASE,
            access_level="read_only",
            project_id="project-123",
        )
        assert policy.name == "db-access"
        assert policy.environment == "staging"
        assert len(policy.rules) == 1
        assert policy.rules[0].service == ServiceType.DATABASE
        assert policy.rules[0].access_level == "read_only"

    def test_create_evalap_service_policy(self):
        """Test create_evalap_service_policy function."""
        policy = create_evalap_service_policy(
            environment="production",
            project_id="project-123",
        )
        assert policy.name == "evalap-service"
        assert policy.environment == "production"
        assert len(policy.rules) == 6  # 6 services configured

        # Verify services included
        services = {rule.service for rule in policy.rules}
        assert ServiceType.SERVERLESS_CONTAINERS in services
        assert ServiceType.DATABASE in services
        assert ServiceType.OBJECT_STORAGE in services
        assert ServiceType.SECRET_MANAGER in services
        assert ServiceType.CONTAINER_REGISTRY in services
        assert ServiceType.COCKPIT in services

        # Verify least privilege (secret_manager should be secret_access, not full_access)
        secret_rule = next(r for r in policy.rules if r.service == ServiceType.SECRET_MANAGER)
        assert secret_rule.access_level == "secret_access"

        # Verify container_registry is read_only
        registry_rule = next(r for r in policy.rules if r.service == ServiceType.CONTAINER_REGISTRY)
        assert registry_rule.access_level == "read_only"

    def test_create_ci_cd_policy(self):
        """Test create_ci_cd_policy function."""
        policy = create_ci_cd_policy(
            environment="staging",
            project_id="project-123",
        )
        assert policy.name == "evalap-cicd"
        assert len(policy.rules) == 4

        # Verify services included
        services = {rule.service for rule in policy.rules}
        assert ServiceType.SERVERLESS_CONTAINERS in services
        assert ServiceType.CONTAINER_REGISTRY in services
        assert ServiceType.SECRET_MANAGER in services
        assert ServiceType.COCKPIT in services

        # Verify secret_manager is read_only for CI/CD
        secret_rule = next(r for r in policy.rules if r.service == ServiceType.SECRET_MANAGER)
        assert secret_rule.access_level == "read_only"

    def test_create_readonly_policy_all_services(self):
        """Test create_readonly_policy with all services."""
        policy = create_readonly_policy(
            name="viewer",
            environment="production",
            project_id="project-123",
        )
        assert policy.name == "viewer"

        # All rules should be read_only
        for rule in policy.rules:
            assert rule.access_level == "read_only"

    def test_create_readonly_policy_specific_services(self):
        """Test create_readonly_policy with specific services."""
        policy = create_readonly_policy(
            name="db-viewer",
            environment="dev",
            project_id="project-123",
            services=[ServiceType.DATABASE, ServiceType.COCKPIT],
        )
        assert len(policy.rules) == 2

        services = {rule.service for rule in policy.rules}
        assert ServiceType.DATABASE in services
        assert ServiceType.COCKPIT in services


class TestValidationFunctions:
    """Tests for IAM validation functions."""

    def test_validate_uuid_valid(self):
        """Test valid UUID validation."""
        assert validate_uuid("12345678-1234-1234-1234-123456789abc") is True
        assert validate_uuid("ABCDEF12-3456-7890-ABCD-EF1234567890") is True

    def test_validate_uuid_invalid(self):
        """Test invalid UUID validation."""
        assert validate_uuid("not-a-uuid") is False
        assert validate_uuid("12345678-1234-1234-1234") is False
        assert validate_uuid("") is False

    def test_validate_iam_rule_config_valid(self):
        """Test valid IAM rule config validation."""
        rule = IAMRuleConfig(
            service="database",
            access_level="full_access",
            project_ids=["12345678-1234-1234-1234-123456789abc"],
        )
        assert validate_iam_rule_config(rule) is True

    def test_validate_iam_rule_config_invalid_service(self):
        """Test IAM rule config with invalid service."""
        # Use MagicMock to bypass Pydantic validation and test the validation function directly
        rule = MagicMock()
        rule.service = "invalid_service"
        rule.access_level = "full_access"
        rule.project_ids = ["12345678-1234-1234-1234-123456789abc"]
        rule.organization_id = None

        with pytest.raises(ValueError) as exc_info:
            validate_iam_rule_config(rule)
        assert "Invalid service" in str(exc_info.value)

    def test_validate_iam_rule_config_invalid_access_level(self):
        """Test IAM rule config with invalid access level."""
        rule = MagicMock()
        rule.service = "database"
        rule.access_level = "invalid_level"
        rule.project_ids = ["12345678-1234-1234-1234-123456789abc"]
        rule.organization_id = None

        with pytest.raises(ValueError) as exc_info:
            validate_iam_rule_config(rule)
        assert "Invalid access level" in str(exc_info.value)

    def test_validate_iam_rule_config_no_scope(self):
        """Test IAM rule config with no scope."""
        rule = MagicMock()
        rule.service = "database"
        rule.access_level = "full_access"
        rule.project_ids = None
        rule.organization_id = None

        with pytest.raises(ValueError) as exc_info:
            validate_iam_rule_config(rule)
        assert "Must specify either" in str(exc_info.value)

    def test_validate_iam_rule_config_both_scopes(self):
        """Test IAM rule config with both scopes."""
        rule = MagicMock()
        rule.service = "database"
        rule.access_level = "full_access"
        rule.project_ids = ["12345678-1234-1234-1234-123456789abc"]
        rule.organization_id = "12345678-1234-1234-1234-123456789abc"

        with pytest.raises(ValueError) as exc_info:
            validate_iam_rule_config(rule)
        assert "Cannot specify both" in str(exc_info.value)

    def test_validate_iam_policy_config_valid(self):
        """Test valid IAM policy config validation."""
        rule = MagicMock()
        rule.service = "database"
        rule.access_level = "full_access"
        rule.project_ids = ["12345678-1234-1234-1234-123456789abc"]
        rule.organization_id = None

        config = MagicMock()
        config.name = "test-policy"
        config.description = "Test policy"
        config.rules = [rule]

        assert validate_iam_policy_config(config) is True

    def test_validate_iam_policy_config_empty_name(self):
        """Test IAM policy config with empty name."""
        config = MagicMock()
        config.name = ""
        config.description = "Test policy"
        config.rules = []

        with pytest.raises(ValueError) as exc_info:
            validate_iam_policy_config(config)
        assert "name cannot be empty" in str(exc_info.value)

    def test_validate_iam_policy_config_no_rules(self):
        """Test IAM policy config with no rules."""
        config = MagicMock()
        config.name = "test-policy"
        config.description = "Test policy"
        config.rules = []

        with pytest.raises(ValueError) as exc_info:
            validate_iam_policy_config(config)
        assert "at least one rule" in str(exc_info.value)

    def test_validate_least_privilege_valid(self):
        """Test valid least privilege validation."""
        rule1 = MagicMock()
        rule1.service = "database"
        rule1.organization_id = None

        rule2 = MagicMock()
        rule2.service = "object_storage"
        rule2.organization_id = None

        rules = [rule1, rule2]
        required = ["database", "object_storage"]

        assert validate_least_privilege(rules, required) is True

    def test_validate_least_privilege_unnecessary_service(self):
        """Test least privilege with unnecessary service."""
        rule1 = MagicMock()
        rule1.service = "database"
        rule1.organization_id = None

        rule2 = MagicMock()
        rule2.service = "cockpit"  # Not required
        rule2.organization_id = None

        rules = [rule1, rule2]
        required = ["database"]

        with pytest.raises(ValueError) as exc_info:
            validate_least_privilege(rules, required)
        assert "unnecessary services" in str(exc_info.value)

    def test_validate_least_privilege_org_wide_access(self):
        """Test least privilege with organization-wide access."""
        rule = MagicMock()
        rule.service = "database"
        rule.organization_id = "org-123"

        rules = [rule]
        required = ["database"]

        with pytest.raises(ValueError) as exc_info:
            validate_least_privilege(rules, required)
        assert "organization-wide access" in str(exc_info.value)


class TestIAMRuleConfigModel:
    """Tests for IAMRuleConfig Pydantic model."""

    def test_valid_rule_config(self):
        """Test valid IAMRuleConfig creation."""
        config = IAMRuleConfig(
            service="database",
            access_level="full_access",
            project_ids=["project-123"],
        )
        assert config.service == "database"
        assert config.access_level == "full_access"

    def test_invalid_service_raises_validation_error(self):
        """Test that invalid service raises validation error."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            IAMRuleConfig(
                service="invalid_service",
                access_level="full_access",
                project_ids=["project-123"],
            )
        assert "Service must be one of" in str(exc_info.value)


class TestIAMPolicyConfigModel:
    """Tests for IAMPolicyConfig Pydantic model."""

    def test_valid_policy_config(self):
        """Test valid IAMPolicyConfig creation."""
        rule = IAMRuleConfig(
            service="database",
            access_level="full_access",
            project_ids=["project-123"],
        )
        config = IAMPolicyConfigModel(
            name="test-policy",
            description="Test policy",
            rules=[rule],
        )
        assert config.name == "test-policy"
        assert config.description == "Test policy"
        assert len(config.rules) == 1
        assert config.create_api_key is False

    def test_policy_config_with_api_key(self):
        """Test IAMPolicyConfig with API key creation."""
        rule = IAMRuleConfig(
            service="object_storage",
            access_level="read_only",
            project_ids=["project-123"],
        )
        config = IAMPolicyConfigModel(
            name="storage-reader",
            description="Read-only storage access",
            rules=[rule],
            create_api_key=True,
        )
        assert config.create_api_key is True


class TestScalewayPermissionSetsValidation:
    """Tests for Scaleway permission sets in validation module."""

    def test_permission_sets_match_component(self):
        """Test that validation permission sets match component permission sets."""
        # Verify all services are present in both
        component_services = {s.value for s in ServiceType}
        validation_services = set(SCALEWAY_PERMISSION_SETS.keys())

        assert component_services == validation_services

    def test_all_access_levels_present(self):
        """Test that all services have at least full_access and read_only."""
        for service, levels in SCALEWAY_PERMISSION_SETS.items():
            assert "full_access" in levels, f"{service} missing full_access"
            assert "read_only" in levels, f"{service} missing read_only"
