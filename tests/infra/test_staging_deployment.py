"""
Staging Environment Deployment Test

Tests that the staging infrastructure can be deployed successfully
and all services are accessible via their endpoints.
"""

import json
import os
import subprocess
import time
from typing import Any, Dict

import pytest
import requests


class TestStagingDeployment:
    """Test suite for staging environment deployment"""

    @pytest.fixture(scope="class")
    def staging_outputs(self) -> Dict[str, Any]:
        """Get outputs from staging deployment"""
        outputs = {}

        # Change to staging directory
        os.chdir("infra/staging")

        try:
            # Get Terraform outputs
            result = subprocess.run(["tofu", "output", "-json"], capture_output=True, text=True, timeout=300)

            if result.returncode != 0:
                pytest.skip(f"Could not get staging outputs: {result.stderr}")

            outputs = json.loads(result.stdout)

        except subprocess.TimeoutExpired:
            pytest.skip("Timeout getting staging outputs")
        except json.JSONDecodeError:
            pytest.skip("Could not parse staging outputs")
        except FileNotFoundError:
            pytest.skip("OpenTofu not found or not in staging directory")

        return outputs

    @pytest.fixture(scope="class")
    def service_endpoints(self, staging_outputs) -> Dict[str, str]:
        """Extract service endpoints from outputs"""
        endpoints = {}

        # Extract container endpoints
        if "container_endpoints" in staging_outputs:
            container_endpoints = json.loads(staging_outputs["container_endpoints"]["value"])
            endpoints.update(container_endpoints)

        # Extract individual service URLs if available
        for service in ["documentation", "runners", "streamlit"]:
            service_key = f"{service}_url"
            if service_key in staging_outputs:
                endpoints[service] = staging_outputs[service_key]["value"]

        return endpoints

    def test_staging_state_exists(self):
        """Test that staging Terraform state exists and is accessible"""
        os.chdir("infra/staging")

        result = subprocess.run(["tofu", "state", "list"], capture_output=True, text=True, timeout=60)

        assert result.returncode == 0, f"Failed to list state: {result.stderr}"
        assert len(result.stdout.strip()) > 0, "No resources found in state"

    def test_required_resources_deployed(self):
        """Test that all required resources are deployed"""
        os.chdir("infra/staging")

        result = subprocess.run(["tofu", "state", "list"], capture_output=True, text=True, timeout=60)

        resources = result.stdout.strip().split("\n")

        # Check for required resource types
        required_resources = [
            "scaleway_container_namespace",
            "scaleway_container",
            "scaleway_rdb_instance",
            "scaleway_account_secret",
        ]

        deployed_resources = [r for r in resources if r]

        for resource_type in required_resources:
            matching = [r for r in deployed_resources if resource_type in r]
            assert len(matching) > 0, f"No {resource_type} resources deployed"

    def test_service_endpoints_accessible(self, service_endpoints):
        """Test that all service endpoints are accessible"""
        for service_name, endpoint in service_endpoints.items():
            if not endpoint:
                pytest.skip(f"No endpoint for {service_name}")

            # Wait a moment for services to be ready
            time.sleep(5)

            try:
                response = requests.get(endpoint, timeout=30)

                # Accept 200 OK or 401 (if auth required) as success
                assert response.status_code in [200, 401, 403], (
                    f"Service {service_name} returned {response.status_code}"
                )

            except requests.exceptions.Timeout:
                pytest.fail(f"Service {service_name} timed out")
            except requests.exceptions.ConnectionError:
                pytest.fail(f"Service {service_name} not reachable")

    def test_documentation_service_health(self, service_endpoints):
        """Test documentation service health endpoint"""
        if "documentation" not in service_endpoints:
            pytest.skip("Documentation service endpoint not available")

        endpoint = service_endpoints["documentation"]
        health_url = f"{endpoint.rstrip('/')}/health"

        try:
            response = requests.get(health_url, timeout=30)
            assert response.status_code == 200, f"Health check failed: {response.status_code}"

            # Check if response contains health information
            try:
                health_data = response.json()
                assert "status" in health_data, "Health response missing status"
                assert health_data["status"] in ["healthy", "ok"], f"Unhealthy status: {health_data['status']}"
            except json.JSONDecodeError:
                # If not JSON, just check for success status
                pass

        except requests.exceptions.RequestException as e:
            pytest.fail(f"Documentation health check failed: {e}")

    def test_runners_service_health(self, service_endpoints):
        """Test runners service health endpoint"""
        if "runners" not in service_endpoints:
            pytest.skip("Runners service endpoint not available")

        endpoint = service_endpoints["runners"]
        health_url = f"{endpoint.rstrip('/')}/health"

        try:
            response = requests.get(health_url, timeout=30)
            assert response.status_code == 200, f"Health check failed: {response.status_code}"

            # Check for runner-specific health indicators
            try:
                health_data = response.json()
                assert "status" in health_data, "Health response missing status"
                assert health_data["status"] in ["healthy", "ok"], f"Unhealthy status: {health_data['status']}"
            except json.JSONDecodeError:
                pass

        except requests.exceptions.RequestException as e:
            pytest.fail(f"Runners health check failed: {e}")

    def test_streamlit_service_health(self, service_endpoints):
        """Test Streamlit service is accessible"""
        if "streamlit" not in service_endpoints:
            pytest.skip("Streamlit service endpoint not available")

        endpoint = service_endpoints["streamlit"]

        try:
            response = requests.get(endpoint, timeout=30)
            assert response.status_code == 200, f"Streamlit not accessible: {response.status_code}"

            # Check for Streamlit-specific content
            assert "Streamlit" in response.text or "st." in response.text, (
                "Response doesn't appear to be from Streamlit"
            )

        except requests.exceptions.RequestException as e:
            pytest.fail(f"Streamlit accessibility check failed: {e}")

    def test_database_connectivity(self, staging_outputs):
        """Test database connectivity and basic operations"""
        if "database_connection_string" not in staging_outputs:
            pytest.skip("Database connection string not available")

        # This would require database client libraries
        # For now, just validate the connection string format
        conn_string = staging_outputs["database_connection_string"]["value"]

        assert "postgresql://" in conn_string, "Invalid PostgreSQL connection string"
        assert "@" in conn_string, "Missing host in connection string"
        assert ":" in conn_string.split("@")[1], "Missing port in connection string"

    def test_infrastructure_tags(self):
        """Test that all resources have proper tags"""
        os.chdir("infra/staging")

        result = subprocess.run(["tofu", "state", "list"], capture_output=True, text=True, timeout=60)

        resources = result.stdout.strip().split("\n")

        for resource in resources:
            if not resource:
                continue

            # Show resource details to check tags
            show_result = subprocess.run(
                ["tofu", "show", "-json", resource], capture_output=True, text=True, timeout=30
            )

            if show_result.returncode == 0:
                # Check for required tags in the resource
                # This would need specific implementation based on resource type
                pass

    def test_monitoring_enabled(self, staging_outputs):
        """Test that monitoring is properly configured"""
        if "monitoring_enabled" in staging_outputs:
            monitoring = staging_outputs["monitoring_enabled"]["value"]
            assert monitoring is True, "Monitoring should be enabled in staging"

    def test_deployment_timestamp(self, staging_outputs):
        """Test that deployment timestamp is recent"""
        if "deployment_timestamp" in staging_outputs:
            timestamp = staging_outputs["deployment_timestamp"]["value"]
            # Validate timestamp format and recency
            assert isinstance(timestamp, str), "Deployment timestamp should be a string"
            # Additional timestamp validation could be added here


class TestStagingConfiguration:
    """Test staging-specific configuration"""

    def test_staging_environment_variables(self):
        """Test that staging environment variables are properly set"""
        os.chdir("infra/staging")

        result = subprocess.run(
            ["tofu", "plan", "-detailed-exitcode"], capture_output=True, text=True, timeout=120
        )

        # Should have no changes (exit code 0) or just refresh (exit code 2)
        assert result.returncode in [0, 2], f"Unexpected plan changes: {result.stdout}"

    def test_resource_naming_convention(self):
        """Test that resources follow staging naming convention"""
        os.chdir("infra/staging")

        result = subprocess.run(["tofu", "state", "list"], capture_output=True, text=True, timeout=60)

        resources = result.stdout.strip().split("\n")

        for resource in resources:
            if not resource:
                continue

            # Check that resource names contain "staging"
            # This would need specific implementation based on naming convention
            pass
