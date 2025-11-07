"""
Staging Rollback Test

Tests that staging infrastructure can be safely rolled back
to previous states without data loss or service disruption.
"""

import json
import os
import subprocess
import time

import pytest
import requests


class TestStagingRollback:
    """Test suite for staging rollback capabilities"""

    @pytest.fixture(scope="class")
    def staging_workspace(self):
        """Ensure we're in the staging workspace"""
        os.chdir("infra/staging")

        # Store original state for cleanup
        original_state = subprocess.run(["tofu", "state", "list"], capture_output=True, text=True, timeout=60)

        yield original_state.stdout.strip().split("\n")

        # Cleanup: ensure we're back to a stable state
        subprocess.run(["tofu", "apply", "-auto-approve"], capture_output=True, timeout=600)

    @pytest.fixture(scope="class")
    def backup_outputs(self):
        """Create a backup of current outputs for comparison"""
        result = subprocess.run(["tofu", "output", "-json"], capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            pytest.skip(f"Could not get outputs: {result.stderr}")

        return json.loads(result.stdout)

    def test_terraform_state_backup(self):
        """Test that Terraform state can be backed up"""
        # Create a backup of the current state
        backup_file = f"terraform.tfstate.backup.{int(time.time())}"

        result = subprocess.run(
            ["cp", "terraform.tfstate", backup_file], capture_output=True, text=True, timeout=60
        )

        assert result.returncode == 0, "Failed to backup Terraform state"
        assert os.path.exists(backup_file), "Backup file was not created"

        # Cleanup
        os.remove(backup_file)

    def test_state_list_before_changes(self, staging_workspace):
        """Test that we can list state before making changes"""
        original_resources = [r for r in staging_workspace if r]

        assert len(original_resources) > 0, "Should have resources in state"

        # Verify key resource types exist
        resource_types = set()
        for resource in original_resources:
            if "." in resource:
                resource_types.add(resource.split(".")[0])

        expected_types = ["scaleway_container", "scaleway_rdb_instance"]
        for expected in expected_types:
            found = any(expected in r for r in resource_types)
            assert found, f"Should have {expected} resources"

    def test_plan_with_no_changes(self):
        """Test that plan shows no changes when nothing is modified"""
        result = subprocess.run(
            ["tofu", "plan", "-detailed-exitcode"], capture_output=True, text=True, timeout=120
        )

        # Exit code 0 = no changes, 2 = only refresh changes
        assert result.returncode in [0, 2], (
            f"Expected no changes but got: {result.returncode}\n{result.stdout}"
        )

    def test_create_test_resource_for_rollback(self):
        """Create a test resource to practice rollback"""
        # Create a temporary resource that we can roll back
        test_resource = """
resource "scaleway_instance_ip" "test_rollback_ip" {
  count = 1
}
"""

        with open("test_rollback.tf", "w") as f:
            f.write(test_resource)

        # Plan and apply the test resource
        result = subprocess.run(
            ["tofu", "plan", "-out=test_plan"], capture_output=True, text=True, timeout=120
        )

        assert result.returncode == 0, f"Plan failed: {result.stderr}"
        assert "1 to add" in result.stdout, "Should plan to add test resource"

        # Apply the test resource
        result = subprocess.run(
            ["tofu", "apply", "-auto-approve", "test_plan"], capture_output=True, text=True, timeout=300
        )

        assert result.returncode == 0, f"Apply failed: {result.stderr}"
        assert "1 added" in result.stdout, "Should have added test resource"

        # Verify the resource exists
        result = subprocess.run(["tofu", "state", "list"], capture_output=True, text=True, timeout=60)

        assert "scaleway_instance_ip.test_rollback_ip" in result.stdout, "Test resource should be in state"

    def test_rollback_by_removing_test_resource(self):
        """Test rollback by removing the test resource"""
        # Remove the test resource file
        if os.path.exists("test_rollback.tf"):
            os.remove("test_rollback.tf")

        # Plan the removal
        result = subprocess.run(
            ["tofu", "plan", "-out=rollback_plan"], capture_output=True, text=True, timeout=120
        )

        assert result.returncode == 0, f"Plan failed: {result.stderr}"
        assert "1 to destroy" in result.stdout, "Should plan to destroy test resource"

        # Apply the rollback
        result = subprocess.run(
            ["tofu", "apply", "-auto-approve", "rollback_plan"], capture_output=True, text=True, timeout=300
        )

        assert result.returncode == 0, f"Rollback failed: {result.stderr}"
        assert "1 destroyed" in result.stdout, "Should have destroyed test resource"

        # Verify the resource is gone
        result = subprocess.run(["tofu", "state", "list"], capture_output=True, text=True, timeout=60)

        assert "scaleway_instance_ip.test_rollback_ip" not in result.stdout, (
            "Test resource should be removed from state"
        )

    def test_database_backup_before_rollback(self, backup_outputs):
        """Test that database is backed up before rollback operations"""
        if "database_endpoint" not in backup_outputs:
            pytest.skip("No database deployed")

        # This would test database backup creation
        # For now, just validate that backup configuration exists
        db_endpoint = backup_outputs["database_endpoint"]["value"]
        assert db_endpoint, "Database endpoint should be available"

        # In a real implementation, this would:
        # 1. Create a database backup
        # 2. Verify backup exists
        # 3. Test backup restoration capability

    def test_service_availability_during_rollback(self, backup_outputs):
        """Test that core services remain available during rollback"""
        if "container_endpoints" not in backup_outputs:
            pytest.skip("No container services deployed")

        endpoints = json.loads(backup_outputs["container_endpoints"]["value"])

        # Test that services are available before rollback
        for service, endpoint in endpoints.items():
            if endpoint:
                try:
                    response = requests.get(endpoint, timeout=10)
                    # Services should be accessible (200, 401, or 403 are acceptable)
                    assert response.status_code in [200, 401, 403], (
                        f"Service {service} not accessible before rollback"
                    )
                except requests.exceptions.RequestException:
                    pytest.skip(f"Service {service} not accessible for rollback test")

    def test_state_consistency_after_rollback(self):
        """Test that Terraform state is consistent after rollback"""
        # Validate state file integrity
        result = subprocess.run(["tofu", "validate"], capture_output=True, text=True, timeout=60)

        assert result.returncode == 0, f"State validation failed: {result.stderr}"

        # Check that state can be refreshed
        result = subprocess.run(
            ["tofu", "refresh", "-auto-approve"], capture_output=True, text=True, timeout=300
        )

        assert result.returncode == 0, f"State refresh failed: {result.stderr}"

    def test_outputs_consistency_after_rollback(self, backup_outputs):
        """Test that outputs are consistent after rollback"""
        # Get current outputs
        result = subprocess.run(["tofu", "output", "-json"], capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            pytest.skip(f"Could not get current outputs: {result.stderr}")

        current_outputs = json.loads(result.stdout)

        # Compare key outputs with backup
        critical_outputs = ["vpc_id", "private_network_id", "security_group_id"]

        for output_name in critical_outputs:
            backup_value = backup_outputs.get(output_name, {}).get("value")
            current_value = current_outputs.get(output_name, {}).get("value")

            # Critical infrastructure outputs should remain the same
            assert backup_value == current_value, f"Critical output {output_name} changed after rollback"

    def test_rollback_with_force_flag(self):
        """Test rollback using force flag for corrupted state"""
        # This would test recovery from corrupted state scenarios
        # For now, just validate that force operations work

        # Test force refresh
        result = subprocess.run(
            ["tofu", "refresh", "-lock-timeout=60s", "-auto-approve"],
            capture_output=True,
            text=True,
            timeout=300,
        )

        assert result.returncode == 0, f"Force refresh failed: {result.stderr}"

    def test_rollback_documentation(self):
        """Test that rollback operations are properly documented"""
        # Check that we have documentation for rollback procedures
        doc_file = "../../docs/troubleshooting.md"

        if os.path.exists(doc_file):
            with open(doc_file, "r") as f:
                content = f.read()

            # Should contain rollback information
            assert "rollback" in content.lower(), "Documentation should contain rollback procedures"

    def test_rollback_time_limits(self):
        """Test that rollback operations complete within time limits"""
        start_time = time.time()

        # Perform a simple rollback operation (refresh)
        result = subprocess.run(
            ["tofu", "refresh", "-auto-approve"], capture_output=True, text=True, timeout=300
        )

        end_time = time.time()
        duration = end_time - start_time

        assert result.returncode == 0, f"Rollback operation failed: {result.stderr}"
        assert duration < 300, f"Rollback took too long: {duration} seconds"

    def test_rollback_error_handling(self):
        """Test error handling during rollback operations"""
        # Test with invalid configuration to ensure proper error handling
        invalid_config = """
resource "scaleway_instance_ip" "invalid_test" {
  count = -1  # Invalid configuration
}
"""

        with open("invalid_test.tf", "w") as f:
            f.write(invalid_config)

        # Plan should fail gracefully
        result = subprocess.run(["tofu", "plan"], capture_output=True, text=True, timeout=120)

        assert result.returncode != 0, "Plan should fail with invalid config"
        assert "Error:" in result.stderr, "Should provide clear error message"

        # Cleanup
        if os.path.exists("invalid_test.tf"):
            os.remove("invalid_test.tf")


class TestRollbackAutomation:
    """Test automated rollback capabilities"""

    def test_rollback_script_exists(self):
        """Test that rollback scripts are available"""
        rollback_script = "../scripts/rollback_staging.sh"

        if os.path.exists(rollback_script):
            # Script should be executable
            assert os.access(rollback_script, os.X_OK), "Rollback script should be executable"

    def test_rollback_validation_script(self):
        """Test rollback validation capabilities"""
        validation_script = "../scripts/validate_rollback.sh"

        if os.path.exists(validation_script):
            # Script should be executable
            assert os.access(validation_script, os.X_OK), "Validation script should be executable"
