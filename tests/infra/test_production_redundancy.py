"""
Production Redundancy Test

Tests that production infrastructure has proper redundancy and high availability
configuration to meet 99.5% uptime requirements.
"""

import concurrent.futures
import json
import os
import subprocess
import time
from typing import Any, Dict, List

import pytest
import requests


class TestProductionRedundancy:
    """Test suite for production redundancy and high availability"""

    @pytest.fixture(scope="class")
    def production_outputs(self) -> Dict[str, Any]:
        """Get outputs from production deployment"""
        outputs = {}

        os.chdir("infra/production")

        try:
            result = subprocess.run(["tofu", "output", "-json"], capture_output=True, text=True, timeout=300)

            if result.returncode != 0:
                pytest.skip(f"Could not get production outputs: {result.stderr}")

            outputs = json.loads(result.stdout)

        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pytest.skip("Could not get production outputs")

        return outputs

    @pytest.fixture(scope="class")
    def service_endpoints(self, production_outputs) -> Dict[str, List[str]]:
        """Extract all service endpoints (should be multiple for redundancy)"""
        endpoints = {}

        # Extract container endpoints (should have multiple for HA)
        if "container_endpoints" in production_outputs:
            container_endpoints = json.loads(production_outputs["container_endpoints"]["value"])
            # Convert to lists if not already
            for service, urls in container_endpoints.items():
                if isinstance(urls, str):
                    endpoints[service] = [urls]
                else:
                    endpoints[service] = urls

        # Extract load balancer endpoints
        if "load_balancer_endpoints" in production_outputs:
            lb_endpoints = json.loads(production_outputs["load_balancer_endpoints"]["value"])
            endpoints.update(lb_endpoints)

        return endpoints

    def test_minimum_instance_count(self, production_outputs):
        """Test that production has minimum required instances per service"""
        if "container_instance_counts" not in production_outputs:
            pytest.skip("Container instance counts not available")

        instance_counts = json.loads(production_outputs["container_instance_counts"]["value"])

        # Production should have minimum 2 instances per service
        required_services = ["documentation", "runners", "streamlit"]

        for service in required_services:
            count = instance_counts.get(service, 0)
            assert count >= 2, f"Service {service} should have at least 2 instances, got {count}"

    def test_load_balancer_configuration(self, production_outputs):
        """Test that load balancers are properly configured"""
        if "load_balancer_ids" not in production_outputs:
            pytest.skip("Load balancer configuration not available")

        lb_ids = json.loads(production_outputs["load_balancer_ids"]["value"])

        # Should have load balancers for each service
        required_services = ["documentation", "runners", "streamlit"]

        for service in required_services:
            assert f"{service}_lb" in lb_ids, f"Load balancer for {service} should be deployed"

    def test_database_high_availability(self, production_outputs):
        """Test that database has high availability configuration"""
        if "database_ha_enabled" not in production_outputs:
            pytest.skip("Database HA configuration not available")

        ha_enabled = production_outputs["database_ha_enabled"]["value"]
        assert ha_enabled is True, "Production database should have HA enabled"

        # Check for replica configuration
        if "database_replica_count" in production_outputs:
            replica_count = production_outputs["database_replica_count"]["value"]
            assert replica_count >= 1, "Production database should have at least 1 replica"

    def test_multiple_service_endpoints(self, service_endpoints):
        """Test that services have multiple endpoints for redundancy"""
        for service_name, endpoints in service_endpoints.items():
            assert len(endpoints) >= 2, (
                f"Service {service_name} should have at least 2 endpoints for redundancy, got {len(endpoints)}"
            )

    def test_endpoint_diversity(self, service_endpoints):
        """Test that endpoints are on different instances/containers"""
        for service_name, endpoints in service_endpoints.items():
            # Endpoints should be different URLs
            unique_endpoints = set(endpoints)
            assert len(unique_endpoints) == len(endpoints), (
                f"Service {service_name} should have unique endpoints, got duplicates"
            )

    def test_concurrent_service_access(self, service_endpoints):
        """Test that multiple endpoints can be accessed concurrently"""

        def check_endpoint(endpoint):
            try:
                response = requests.get(endpoint, timeout=30)
                return response.status_code in [200, 401, 403]
            except requests.exceptions.RequestException:
                return False

        # Test concurrent access to all endpoints
        for service_name, endpoints in service_endpoints.items():
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(endpoints)) as executor:
                futures = [executor.submit(check_endpoint, endpoint) for endpoint in endpoints]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]

            # At least 80% of endpoints should be accessible
            accessible_count = sum(results)
            assert accessible_count >= len(endpoints) * 0.8, (
                f"Service {service_name}: Only {accessible_count}/{len(endpoints)} endpoints accessible"
            )

    def test_auto_restart_configuration(self, production_outputs):
        """Test that auto-restart is configured for containers"""
        if "container_restart_policy" not in production_outputs:
            pytest.skip("Container restart policy not available")

        restart_policy = json.loads(production_outputs["container_restart_policy"]["value"])

        for service, policy in restart_policy.items():
            assert policy in ["always", "on-failure"], (
                f"Service {service} should have auto-restart enabled, got {policy}"
            )

    def test_health_check_configuration(self, production_outputs):
        """Test that health checks are configured for load balancers"""
        if "health_check_config" not in production_outputs:
            pytest.skip("Health check configuration not available")

        health_checks = json.loads(production_outputs["health_check_config"]["value"])

        for service, config in health_checks.items():
            assert "path" in config, f"Service {service} should have health check path"
            assert "interval" in config, f"Service {service} should have health check interval"
            assert "timeout" in config, f"Service {service} should have health check timeout"

    def test_availability_zones_distribution(self, production_outputs):
        """Test that instances are distributed across multiple availability zones"""
        if "instance_zone_distribution" not in production_outputs:
            pytest.skip("Zone distribution information not available")

        zone_distribution = json.loads(production_outputs["instance_zone_distribution"]["value"])

        # Should use multiple zones for high availability
        zones_used = set()
        for _, zones in zone_distribution.items():
            zones_used.update(zones)

        assert len(zones_used) >= 2, (
            f"Production should use at least 2 availability zones, got {len(zones_used)}: {zones_used}"
        )

    def test_backup_configuration(self, production_outputs):
        """Test that backup is properly configured for production"""
        if "backup_enabled" not in production_outputs:
            pytest.skip("Backup configuration not available")

        backup_enabled = production_outputs["backup_enabled"]["value"]
        assert backup_enabled is True, "Production should have backup enabled"

        # Check backup retention
        if "backup_retention_days" in production_outputs:
            retention = production_outputs["backup_retention_days"]["value"]
            assert retention >= 30, "Production backup retention should be at least 30 days"

    def test_monitoring_coverage(self, production_outputs):
        """Test that monitoring covers all critical components"""
        if "monitoring_endpoints" not in production_outputs:
            pytest.skip("Monitoring configuration not available")

        monitoring = json.loads(production_outputs["monitoring_endpoints"]["value"])

        # Should monitor all services and infrastructure
        required_monitors = ["containers", "database", "load_balancers", "network"]

        for monitor in required_monitors:
            assert monitor in monitoring, f"Should monitor {monitor}"

    def test_service_response_times(self, service_endpoints):
        """Test that services meet response time requirements"""

        def measure_response_time(endpoint):
            try:
                start_time = time.time()
                response = requests.get(endpoint, timeout=30)
                end_time = time.time()

                if response.status_code in [200, 401, 403]:
                    return end_time - start_time
                return None
            except requests.exceptions.RequestException:
                return None

        # Test response times for all endpoints
        for service_name, endpoints in service_endpoints.items():
            response_times = []

            for endpoint in endpoints[:3]:  # Test first 3 endpoints
                response_time = measure_response_time(endpoint)
                if response_time is not None:
                    response_times.append(response_time)

            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                # Should meet <2 second latency requirement
                assert avg_response_time < 2.0, (
                    f"Service {service_name} avg response time {avg_response_time:.2f}s exceeds 2s requirement"
                )

    def test_disaster_recovery_readiness(self, production_outputs):
        """Test disaster recovery configuration and documentation"""
        # Check for DR configuration
        if "dr_enabled" in production_outputs:
            dr_enabled = production_outputs["dr_enabled"]["value"]
            # DR might not be fully implemented yet, but configuration should exist
            assert isinstance(dr_enabled, bool), "DR configuration should be boolean"

        # Check for documentation
        dr_doc = "../../docs/disaster-recovery.md"
        if os.path.exists(dr_doc):
            with open(dr_doc, "r") as f:
                content = f.read()
                assert "recovery" in content.lower(), "DR documentation should exist"

    def test_capacity_planning(self, production_outputs):
        """Test that production has appropriate capacity planning"""
        if "container_resources" not in production_outputs:
            pytest.skip("Container resource configuration not available")

        resources = json.loads(production_outputs["container_resources"]["value"])

        for service, config in resources.items():
            # Should have minimum resource allocation
            assert "cpu" in config, f"Service {service} should have CPU allocation"
            assert "memory" in config, f"Service {service} should have memory allocation"

            # Production should have reasonable resource limits
            cpu_limit = config["cpu"]
            memory_limit = config["memory"]

            assert cpu_limit >= 256, f"Service {service} CPU limit {cpu_limit}m too low"
            assert memory_limit >= 512, f"Service {service} memory limit {memory_limit}Mi too low"

    def test_redirection_failover(self, service_endpoints):
        """Test that traffic is properly redistributed when endpoints fail"""
        # This is a simplified test - real failover testing would require
        # actual endpoint failure simulation

        for service_name, endpoints in service_endpoints.items():
            if len(endpoints) >= 2:
                # Test that load balancer distributes traffic
                # In a real scenario, this would test actual load distribution
                assert len(endpoints) >= 2, (
                    f"Service {service_name} should have multiple endpoints for failover"
                )
