"""
Pytest configuration for infrastructure tests

This file provides common fixtures and configuration for all infrastructure tests.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_path():
    """Get the absolute path to the project root"""
    return project_root


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before running tests"""
    # Ensure we're in the correct directory
    original_dir = os.getcwd()

    # Change to project root
    os.chdir(project_root)

    yield

    # Restore original directory
    os.chdir(original_dir)


@pytest.fixture(scope="session")
def tofu_available():
    """Check if OpenTofu is available"""
    try:
        result = subprocess.run(["tofu", "version"], capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


@pytest.fixture(scope="session")
def terraform_available():
    """Check if Terraform is available (fallback)"""
    try:
        result = subprocess.run(["terraform", "version"], capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


@pytest.fixture(scope="session")
def iac_tool(tofu_available, terraform_available):
    """Get the available IaC tool (prefer OpenTofu)"""
    if tofu_available:
        return "tofu"
    elif terraform_available:
        return "terraform"
    else:
        pytest.skip("Neither OpenTofu nor Terraform is available")


@pytest.fixture(scope="session")
def scaleway_credentials():
    """Check if Scaleway credentials are available"""
    required_vars = ["SCW_ACCESS_KEY", "SCW_SECRET_KEY", "SCW_DEFAULT_PROJECT_ID"]

    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    if missing_vars:
        pytest.skip(f"Missing Scaleway credentials: {', '.join(missing_vars)}")

    return True


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "staging: marks tests that require staging environment")
    config.addinivalue_line("markers", "production: marks tests that require production environment")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers"""
    for item in items:
        # Add integration marker to all infra tests
        item.add_marker(pytest.mark.integration)

        # Add slow marker to tests that might take longer
        if "rollback" in item.name.lower() or "deployment" in item.name.lower():
            item.add_marker(pytest.mark.slow)


@pytest.fixture(scope="function")
def temp_terraform_dir(tmp_path):
    """Create a temporary directory for Terraform operations"""
    tf_dir = tmp_path / "terraform_test"
    tf_dir.mkdir()
    return tf_dir


@pytest.fixture
def mock_scaleway_responses():
    """Mock responses for Scaleway API calls (for unit tests)"""
    # This would contain mock responses for testing without actual API calls
    # Implementation would depend on the testing framework used
    pass


@pytest.fixture(scope="session")
def test_timeout():
    """Default timeout for test operations"""
    return 300  # 5 minutes


@pytest.fixture
def retry_config():
    """Configuration for retry logic in tests"""
    return {"max_attempts": 3, "delay": 5, "backoff": 2}


def pytest_runtest_setup(item):
    """Setup before each test"""
    # Ensure we're in project root
    os.chdir(project_root)

    # Check for required tools based on test markers
    if item.get_closest_marker("staging") or "infra" in item.nodeid:
        if not any([tofu_available(), terraform_available()]):
            pytest.skip("IaC tool required for infrastructure tests")


# Helper functions
def run_command(cmd, timeout=300, capture_output=True, text=True):
    """Run a command with timeout and return result"""
    return subprocess.run(cmd, capture_output=capture_output, text=text, timeout=timeout, shell=True)


def get_terraform_output(output_name=None, workspace="staging"):
    """Get Terraform output from specified workspace"""
    os.chdir(f"infra/{workspace}")

    cmd = ["tofu", "output", "-json"]
    if output_name:
        cmd.append(output_name)

    result = run_command(cmd)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to get output: {result.stderr}")

    if output_name:
        return result.stdout.strip()
    else:
        import json

        return json.loads(result.stdout)


def check_service_health(endpoint, timeout=30):
    """Check if a service endpoint is healthy"""
    import requests

    try:
        response = requests.get(endpoint, timeout=timeout)
        return response.status_code in [200, 401, 403]
    except requests.exceptions.RequestException:
        return False
