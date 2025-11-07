"""
Environment Isolation Test

Tests that staging and production environments are properly isolated
and that staging cannot access production resources.
"""

import json
import os
import subprocess
from typing import Any, Dict

import pytest


class TestEnvironmentIsolation:
    """Test suite for environment isolation"""

    @pytest.fixture(scope="class")
    def staging_outputs(self) -> Dict[str, Any]:
        """Get outputs from staging deployment"""
        outputs = {}

        os.chdir("infra/staging")

        try:
            result = subprocess.run(["tofu", "output", "-json"], capture_output=True, text=True, timeout=300)

            if result.returncode != 0:
                pytest.skip(f"Could not get staging outputs: {result.stderr}")

            outputs = json.loads(result.stdout)

        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pytest.skip("Could not get staging outputs")

        return outputs

    @pytest.fixture(scope="class")
    def production_outputs(self) -> Dict[str, Any]:
        """Get outputs from production deployment (may not exist)"""
        outputs = {}

        # Check if production is deployed
        if not os.path.exists("infra/production"):
            return outputs

        os.chdir("infra/production")

        try:
            result = subprocess.run(["tofu", "output", "-json"], capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                outputs = json.loads(result.stdout)

        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass

        return outputs

    def test_staging_and_production_different_vpcs(self, staging_outputs, production_outputs):
        """Test that staging and production use different VPCs"""
        if not production_outputs:
            pytest.skip("Production not deployed - cannot test VPC isolation")

        staging_vpc = staging_outputs.get("vpc_id", {}).get("value")
        production_vpc = production_outputs.get("vpc_id", {}).get("value")

        assert staging_vpc != production_vpc, "Staging and production should use different VPCs"

    def test_staging_and_production_different_databases(self, staging_outputs, production_outputs):
        """Test that staging and production use different databases"""
        if not production_outputs:
            pytest.skip("Production not deployed - cannot test database isolation")

        staging_db = staging_outputs.get("database_endpoint", {}).get("value")
        production_db = production_outputs.get("database_endpoint", {}).get("value")

        assert staging_db != production_db, "Staging and production should use different databases"

    def test_staging_and_production_different_secrets(self, staging_outputs, production_outputs):
        """Test that staging and production use different secret managers/keys"""
        if not production_outputs:
            pytest.skip("Production not deployed - cannot test secret isolation")

        staging_secrets = staging_outputs.get("secret_manager_id", {}).get("value")
        production_secrets = production_outputs.get("secret_manager_id", {}).get("value")

        assert staging_secrets != production_secrets, (
            "Staging and production should use different secret managers"
        )

    def test_staging_cannot_access_production_endpoints(self, staging_outputs, production_outputs):
        """Test that staging services cannot access production endpoints"""
        if not production_outputs:
            pytest.skip("Production not deployed - cannot test endpoint isolation")

        staging_endpoints = staging_outputs.get("container_endpoints", {}).get("value", {})
        production_endpoints = production_outputs.get("container_endpoints", {}).get("value", {})

        # Test that staging endpoints are different from production
        for service, staging_endpoint in staging_endpoints.items():
            production_endpoint = production_endpoints.get(service)
            if production_endpoint:
                assert staging_endpoint != production_endpoint, (
                    f"Service {service} should have different endpoints in staging and production"
                )

    def test_staging_network_isolation(self, staging_outputs):
        """Test that staging network is properly isolated"""
        staging_vpc = staging_outputs.get("vpc_id", {}).get("value")
        staging_subnet = staging_outputs.get("private_network_id", {}).get("value")

        assert staging_vpc, "Staging VPC should be deployed"
        assert staging_subnet, "Staging private network should be deployed"

        # Validate that the subnet belongs to the VPC
        # This would need additional API calls to validate network topology

    def test_staging_firewall_rules(self, staging_outputs):
        """Test that staging has appropriate firewall rules"""
        staging_sg = staging_outputs.get("security_group_id", {}).get("value")

        assert staging_sg, "Staging security group should be deployed"

        # Check that security group rules are appropriate for staging
        # This would need API calls to inspect security group rules

        # For staging, we might allow more permissive access for testing
        # but production should be more restrictive

    def test_production_more_restrictive_than_staging(self, staging_outputs, production_outputs):
        """Test that production has more restrictive access than staging"""
        if not production_outputs:
            pytest.skip("Production not deployed - cannot compare security")

        # Compare security group configurations
        staging_sg = staging_outputs.get("security_group_id", {}).get("value")
        production_sg = production_outputs.get("security_group_id", {}).get("value")

        assert staging_sg != production_sg, "Staging and production should have different security groups"

        # Production should have more restrictive rules
        # This would need detailed security group inspection

    def test_environment_tag_isolation(self, staging_outputs, production_outputs):
        """Test that resources are properly tagged with environment"""
        staging_tags = staging_outputs.get("resource_tags", {}).get("value", {})
        production_tags = production_outputs.get("resource_tags", {}).get("value", {})

        if staging_tags:
            assert staging_tags.get("Environment") == "staging", (
                "Staging resources should be tagged with Environment=staging"
            )

        if production_tags:
            assert production_tags.get("Environment") == "production", (
                "Production resources should be tagged with Environment=production"
            )

    def test_cross_environment_data_isolation(self):
        """Test that there's no cross-environment data access"""
        # This would test that staging database cannot access production data
        # and vice versa

        # Check database connection strings are different
        os.chdir("infra/staging")

        result = subprocess.run(
            ["tofu", "output", "database_connection_string"], capture_output=True, text=True, timeout=60
        )

        if result.returncode == 0:
            staging_conn = result.stdout.strip()
            assert "staging" in staging_conn.lower(), "Staging database connection should reference staging"

        # Similar check for production if it exists
        if os.path.exists("../production"):
            os.chdir("../production")

            result = subprocess.run(
                ["tofu", "output", "database_connection_string"], capture_output=True, text=True, timeout=60
            )

            if result.returncode == 0:
                production_conn = result.stdout.strip()
                assert "production" in production_conn.lower(), (
                    "Production database connection should reference production"
                )

    def test_monitoring_isolation(self, staging_outputs, production_outputs):
        """Test that monitoring is isolated between environments"""
        staging_monitoring = staging_outputs.get("monitoring_endpoint", {}).get("value")
        production_monitoring = production_outputs.get("monitoring_endpoint", {}).get("value")

        if staging_monitoring and production_monitoring:
            assert staging_monitoring != production_monitoring, (
                "Monitoring endpoints should be different between environments"
            )

    def test_backup_isolation(self, staging_outputs, production_outputs):
        """Test that backups are isolated between environments"""
        staging_backup = staging_outputs.get("backup_bucket", {}).get("value")
        production_backup = production_outputs.get("backup_bucket", {}).get("value")

        if staging_backup and production_backup:
            assert staging_backup != production_backup, (
                "Backup buckets should be different between environments"
            )

    def test_no_shared_resources(self, staging_outputs, production_outputs):
        """Test that no resources are shared between environments"""
        shared_resources = []

        # Check for any overlapping resource IDs
        staging_resources = set()
        production_resources = set()

        # Extract resource identifiers from outputs
        for key, value in staging_outputs.items():
            if isinstance(value, dict) and "value" in value:
                resource_id = value["value"]
                if resource_id and isinstance(resource_id, str):
                    staging_resources.add(resource_id)

        for key, value in production_outputs.items():
            if isinstance(value, dict) and "value" in value:
                resource_id = value["value"]
                if resource_id and isinstance(resource_id, str):
                    production_resources.add(resource_id)

        shared_resources = staging_resources.intersection(production_resources)

        assert len(shared_resources) == 0, f"Found shared resources between environments: {shared_resources}"


class TestStagingSecurityContext:
    """Test staging-specific security context"""

    def test_staging_allows_development_access(self):
        """Test that staging allows development-friendly access"""
        # Staging should allow more permissive access for development
        # but still maintain basic security

        os.chdir("infra/staging")

        # Check that staging has appropriate security group rules
        result = subprocess.run(
            ["tofu", "show", "-json", "scaleway_instance_security_group.main"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            # Validate that staging allows necessary development access
            # This would need inspection of actual security group rules
            pass

    def test_staging_no_production_secrets(self):
        """Test that staging cannot access production secrets"""
        # This would test that staging's secret manager access is limited
        # to staging secrets only

        os.chdir("infra/staging")

        result = subprocess.run(
            ["tofu", "output", "secret_manager_scope"], capture_output=True, text=True, timeout=60
        )

        if result.returncode == 0:
            scope = result.stdout.strip()
            assert "staging" in scope.lower(), "Staging should only access staging secrets"
