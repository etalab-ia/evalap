"""Unit tests for Scaleway helper utilities."""

import pytest

from infra.utils.scaleway_helpers import (
    create_resource_tags,
    format_resource_name,
    validate_bucket_name,
    validate_cpu_memory_combination,
    validate_database_name,
    validate_resource_name,
)


class TestValidateBucketName:
    """Tests for validate_bucket_name function."""

    def test_valid_bucket_name(self):
        """Test that valid bucket names are accepted."""
        assert validate_bucket_name("my-bucket") is True
        assert validate_bucket_name("my-bucket-123") is True
        assert validate_bucket_name("bucket") is True

    def test_bucket_name_with_uppercase(self):
        """Test that uppercase letters are rejected."""
        with pytest.raises(ValueError):
            validate_bucket_name("My-Bucket")

    def test_bucket_name_with_underscore(self):
        """Test that underscores are rejected."""
        with pytest.raises(ValueError):
            validate_bucket_name("my_bucket")

    def test_bucket_name_with_special_chars(self):
        """Test that special characters are rejected."""
        with pytest.raises(ValueError):
            validate_bucket_name("my@bucket")

    def test_bucket_name_too_short(self):
        """Test that names shorter than 3 characters are rejected."""
        with pytest.raises(ValueError):
            validate_bucket_name("ab")

    def test_bucket_name_too_long(self):
        """Test that names longer than 63 characters are rejected."""
        long_name = "a" * 64
        with pytest.raises(ValueError):
            validate_bucket_name(long_name)

    def test_bucket_name_starts_with_dash(self):
        """Test that names starting with dash are rejected."""
        with pytest.raises(ValueError):
            validate_bucket_name("-bucket")

    def test_bucket_name_ends_with_dash(self):
        """Test that names ending with dash are rejected."""
        with pytest.raises(ValueError):
            validate_bucket_name("bucket-")

    def test_bucket_name_consecutive_dashes(self):
        """Test that consecutive dashes are allowed."""
        # Consecutive dashes are actually allowed by the regex
        assert validate_bucket_name("my--bucket") is True


class TestValidateDatabaseName:
    """Tests for validate_database_name function."""

    def test_valid_database_name(self):
        """Test that valid database names are accepted."""
        assert validate_database_name("mydb") is True
        assert validate_database_name("my_database") is True
        assert validate_database_name("db123") is True

    def test_database_name_with_uppercase(self):
        """Test that uppercase letters are accepted."""
        # Database names allow uppercase
        assert validate_database_name("MyDB") is True

    def test_database_name_with_dash(self):
        """Test that dashes are rejected."""
        with pytest.raises(ValueError):
            validate_database_name("my-db")

    def test_database_name_with_special_chars(self):
        """Test that special characters are rejected."""
        with pytest.raises(ValueError):
            validate_database_name("my@db")

    def test_database_name_too_short(self):
        """Test that empty names are rejected."""
        with pytest.raises(ValueError):
            validate_database_name("")

    def test_database_name_too_long(self):
        """Test that names longer than 63 characters are rejected."""
        long_name = "a" * 64
        with pytest.raises(ValueError):
            validate_database_name(long_name)

    def test_database_name_starts_with_number(self):
        """Test that names starting with number are rejected."""
        with pytest.raises(ValueError):
            validate_database_name("1database")

    def test_database_name_starts_with_underscore(self):
        """Test that names starting with underscore are rejected."""
        with pytest.raises(ValueError):
            validate_database_name("_database")


class TestValidateResourceName:
    """Tests for validate_resource_name function."""

    def test_valid_resource_name(self):
        """Test that valid resource names are accepted."""
        assert validate_resource_name("my-resource") is True
        assert validate_resource_name("my_resource") is True
        assert validate_resource_name("resource123") is True

    def test_resource_name_single_char(self):
        """Test that single character names are accepted."""
        assert validate_resource_name("a") is True

    def test_resource_name_too_long(self):
        """Test that names longer than 255 characters are rejected."""
        long_name = "a" * 256
        with pytest.raises(ValueError):
            validate_resource_name(long_name)

    def test_resource_name_empty(self):
        """Test that empty names are rejected."""
        with pytest.raises(ValueError):
            validate_resource_name("")


class TestValidateCpuMemoryCombination:
    """Tests for validate_cpu_memory_combination function."""

    def test_valid_cpu_memory_combinations(self):
        """Test valid CPU/memory combinations."""
        assert validate_cpu_memory_combination(100, 128) is True
        assert validate_cpu_memory_combination(250, 256) is True
        assert validate_cpu_memory_combination(500, 512) is True
        assert validate_cpu_memory_combination(1000, 1024) is True
        assert validate_cpu_memory_combination(2000, 2048) is True
        assert validate_cpu_memory_combination(4000, 4096) is True

    def test_cpu_invalid(self):
        """Test that invalid CPU values are rejected."""
        with pytest.raises(ValueError):
            validate_cpu_memory_combination(50, 512)

    def test_memory_too_low_for_cpu(self):
        """Test that memory below minimum for CPU is rejected."""
        with pytest.raises(ValueError):
            validate_cpu_memory_combination(100, 64)

    def test_memory_too_high_for_cpu(self):
        """Test that memory above maximum for CPU is rejected."""
        with pytest.raises(ValueError):
            validate_cpu_memory_combination(100, 512)

    def test_valid_edge_cases(self):
        """Test valid edge cases."""
        # Minimum CPU with minimum memory
        assert validate_cpu_memory_combination(100, 128) is True
        # Maximum CPU with maximum memory
        assert validate_cpu_memory_combination(4000, 8192) is True


class TestFormatResourceName:
    """Tests for format_resource_name function."""

    def test_format_resource_name_basic(self):
        """Test basic resource name formatting."""
        name = format_resource_name("my-service", "dev")
        assert name == "my-service-dev"

    def test_format_resource_name_uppercase(self):
        """Test that uppercase is converted to lowercase."""
        name = format_resource_name("MyService", "dev")
        assert name == "myservice-dev"

    def test_format_resource_name_underscore(self):
        """Test that underscores are converted to dashes."""
        name = format_resource_name("my_service", "dev")
        assert name == "my-service-dev"

    def test_format_resource_name_with_suffix(self):
        """Test resource name formatting with suffix."""
        name = format_resource_name("service", "prod", suffix="primary")
        assert name == "service-prod-primary"

    def test_format_resource_name_custom_separator(self):
        """Test resource name formatting with custom separator."""
        name = format_resource_name("service", "dev", separator="_")
        assert name == "service_dev"

    def test_format_resource_name_with_numbers(self):
        """Test that numbers are preserved."""
        name = format_resource_name("service123", "dev")
        assert name == "service123-dev"


class TestCreateResourceTags:
    """Tests for create_resource_tags function."""

    def test_create_resource_tags_basic(self):
        """Test creating basic resource tags."""
        tags = create_resource_tags(
            environment="dev",
            component="api",
        )

        assert tags["project"] == "evalap"
        assert tags["environment"] == "dev"
        assert tags["component"] == "api"
        assert tags["managed-by"] == "pulumi"

    def test_create_resource_tags_with_custom_project(self):
        """Test creating tags with custom project."""
        tags = create_resource_tags(
            environment="prod",
            component="database",
            project="my-project",
        )

        assert tags["project"] == "my-project"
        assert tags["environment"] == "prod"
        assert tags["component"] == "database"

    def test_create_resource_tags_with_additional(self):
        """Test creating tags with additional tags."""
        tags = create_resource_tags(
            environment="prod",
            component="database",
            additional_tags={"team": "platform", "cost-center": "engineering"},
        )

        assert tags["project"] == "evalap"
        assert tags["environment"] == "prod"
        assert tags["component"] == "database"
        assert tags["team"] == "platform"
        assert tags["cost-center"] == "engineering"

    def test_create_resource_tags_standard_fields(self):
        """Test that standard fields are always present."""
        tags = create_resource_tags(
            environment="dev",
            component="test",
        )

        assert "project" in tags
        assert "environment" in tags
        assert "component" in tags
        assert "managed-by" in tags
        assert tags["managed-by"] == "pulumi"

    def test_create_resource_tags_different_environments(self):
        """Test tags with different environments."""
        for env in ["dev", "staging", "production"]:
            tags = create_resource_tags(
                environment=env,
                component="service",
            )
            assert tags["environment"] == env

    def test_create_resource_tags_different_components(self):
        """Test tags with different components."""
        for component in ["api", "database", "storage", "network"]:
            tags = create_resource_tags(
                environment="dev",
                component=component,
            )
            assert tags["component"] == component
