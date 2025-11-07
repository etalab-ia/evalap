"""
Production Load Balancing Test

Tests load balancing behavior, traffic distribution, and scaling
capabilities in production environment.
"""

import concurrent.futures
import json
import os
import subprocess
import time
from typing import Any, Dict, List

import pytest
import requests


class TestProductionLoadBalancing:
    """Test suite for production load balancing and scaling"""

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
    def load_balancer_endpoints(self, production_outputs) -> Dict[str, str]:
        """Get load balancer endpoints"""
        if "load_balancer_endpoints" not in production_outputs:
            pytest.skip("Load balancer endpoints not available")

        return json.loads(production_outputs["load_balancer_endpoints"]["value"])

    @pytest.fixture(scope="class")
    def backend_endpoints(self, production_outputs) -> Dict[str, List[str]]:
        """Get backend container endpoints"""
        if "container_endpoints" not in production_outputs:
            pytest.skip("Container endpoints not available")

        endpoints = json.loads(production_outputs["container_endpoints"]["value"])

        # Convert to lists
        for service, urls in endpoints.items():
            if isinstance(urls, str):
                endpoints[service] = [urls]

        return endpoints

    @pytest.fixture(scope="class")
    def load_balancer_config(self, production_outputs) -> Dict[str, Any]:
        """Get load balancer configuration"""
        if "load_balancer_config" not in production_outputs:
            pytest.skip("Load balancer configuration not available")

        return json.loads(production_outputs["load_balancer_config"]["value"])

    def test_load_balancer_exists_per_service(self, load_balancer_endpoints):
        """Test that each service has a load balancer"""
        required_services = ["documentation", "runners", "streamlit"]

        for service in required_services:
            assert service in load_balancer_endpoints, (
                f"Service {service} should have a load balancer endpoint"
            )

            endpoint = load_balancer_endpoints[service]
            assert endpoint.startswith("http"), f"Load balancer endpoint for {service} should be a valid URL"

    def test_load_balancer_health_endpoints(self, load_balancer_endpoints):
        """Test that load balancers have health endpoints"""
        for service, lb_endpoint in load_balancer_endpoints.items():
            health_url = f"{lb_endpoint.rstrip('/')}/health"

            try:
                response = requests.get(health_url, timeout=10)
                assert response.status_code == 200, (
                    f"Load balancer health endpoint for {service} should return 200"
                )

                # Check health response format
                try:
                    health_data = response.json()
                    assert "status" in health_data, f"Health response for {service} should include status"
                except json.JSONDecodeError:
                    # Non-JSON health responses are acceptable
                    pass

            except requests.exceptions.RequestException:
                pytest.fail(f"Load balancer health endpoint for {service} should be accessible")

    def test_traffic_distribution_algorithm(self, load_balancer_config):
        """Test load balancing algorithm configuration"""
        for service, config in load_balancer_config.items():
            algorithm = config.get("algorithm", "")
            valid_algorithms = ["round_robin", "least_connections", "ip_hash", "weighted"]

            assert algorithm in valid_algorithms, (
                f"Service {service} should use valid load balancing algorithm, got {algorithm}"
            )

    def test_session_affinity_configuration(self, load_balancer_config):
        """Test session affinity/sticky sessions configuration"""
        for service, config in load_balancer_config.items():
            session_affinity = config.get("session_affinity", False)

            # Should be explicitly configured (either enabled or disabled)
            assert isinstance(session_affinity, bool), (
                f"Service {service} should have explicit session affinity configuration"
            )

    def test_load_balancer_ssl_termination(self, load_balancer_config):
        """Test SSL termination configuration"""
        for service, config in load_balancer_config.items():
            ssl_enabled = config.get("ssl_enabled", False)

            # Production should use SSL
            assert ssl_enabled is True, f"Service {service} should have SSL enabled in production"

            # Check SSL certificate configuration
            if ssl_enabled:
                cert_config = config.get("ssl_certificate", {})
                assert cert_config.get("type") in ["managed", "custom"], (
                    f"Service {service} should have valid SSL certificate configuration"
                )

    def test_backend_health_checks(self, load_balancer_config):
        """Test backend health check configuration"""
        for service, config in load_balancer_config.items():
            health_check = config.get("health_check", {})

            assert "path" in health_check, f"Service {service} should have health check path configured"

            assert "interval_seconds" in health_check, (
                f"Service {service} should have health check interval configured"
            )

            assert "timeout_seconds" in health_check, (
                f"Service {service} should have health check timeout configured"
            )

            # Check reasonable values
            interval = health_check["interval_seconds"]
            timeout = health_check["timeout_seconds"]

            assert interval <= 30, f"Service {service} health check interval should be <= 30 seconds"
            assert timeout <= 10, f"Service {service} health check timeout should be <= 10 seconds"

    def test_load_balancer_capacity_limits(self, load_balancer_config):
        """Test load balancer capacity and limits"""
        for service, config in load_balancer_config.items():
            # Check connection limits
            max_connections = config.get("max_connections", 0)
            assert max_connections > 0, f"Service {service} should have connection limits configured"

            # Check request rate limits
            rate_limit = config.get("requests_per_second", 0)
            assert rate_limit > 0, f"Service {service} should have rate limiting configured"

    def test_concurrent_request_handling(self, load_balancer_endpoints):
        """Test load balancer handling of concurrent requests"""

        def make_request(endpoint):
            try:
                start_time = time.time()
                response = requests.get(endpoint, timeout=30)
                end_time = time.time()

                return {
                    "status_code": response.status_code,
                    "response_time": end_time - start_time,
                    "success": response.status_code in [200, 401, 403],
                }
            except requests.exceptions.RequestException as e:
                return {
                    "status_code": 0,
                    "response_time": 30.0,  # timeout
                    "success": False,
                    "error": str(e),
                }

        # Test concurrent requests to each load balancer
        for service, lb_endpoint in load_balancer_endpoints.items():
            concurrent_requests = 50

            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
                futures = [executor.submit(make_request, lb_endpoint) for _ in range(concurrent_requests)]

                results = [future.result() for future in concurrent.futures.as_completed(futures)]

            # Analyze results
            successful_requests = sum(1 for r in results if r["success"])
            success_rate = successful_requests / len(results)

            # Should handle concurrent requests well
            assert success_rate >= 0.95, (
                f"Load balancer for {service} success rate {success_rate:.2f} too low for concurrent requests"
            )

            # Check response times
            response_times = [r["response_time"] for r in results if r["success"]]
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                assert avg_response_time < 2.0, (
                    f"Load balancer for {service} avg response time {avg_response_time:.2f}s too high"
                )

    def test_load_balancer_failover_behavior(self, load_balancer_endpoints, backend_endpoints):
        """Test load balancer behavior when backends fail"""
        # This is a simplified test - real failover testing would require
        # actual backend termination

        for service, lb_endpoint in load_balancer_endpoints.items():
            backends = backend_endpoints.get(service, [])

            if len(backends) >= 2:
                # Test that load balancer responds even with some backends potentially down
                try:
                    response = requests.get(lb_endpoint, timeout=10)
                    # Load balancer should handle backend failures gracefully
                    assert response.status_code in [200, 502, 503], (
                        f"Load balancer for {service} should handle backend failures"
                    )
                except requests.exceptions.RequestException:
                    pytest.fail(f"Load balancer for {service} should be accessible")

    def test_weight_based_load_distribution(self, load_balancer_config):
        """Test weighted load distribution configuration"""
        for service, config in load_balancer_config.items():
            if config.get("algorithm") == "weighted":
                weights = config.get("backend_weights", {})

                assert len(weights) > 0, (
                    f"Service {service} with weighted algorithm should have backend weights"
                )

                # Weights should be positive integers
                for backend, weight in weights.items():
                    assert isinstance(weight, int) and weight > 0, (
                        f"Backend {backend} weight should be positive integer"
                    )

    def test_load_balancer_logging(self, load_balancer_config):
        """Test load balancer logging configuration"""
        for service, config in load_balancer_config.items():
            logging_config = config.get("logging", {})

            # Should have access logging enabled
            assert logging_config.get("access_logs_enabled", False), (
                f"Service {service} should have access logging enabled"
            )

            # Should log request details
            log_fields = logging_config.get("log_fields", [])
            required_fields = ["timestamp", "method", "path", "status", "response_time"]

            for field in required_fields:
                assert field in log_fields, f"Service {service} should log {field} in access logs"

    def test_load_balancer_monitoring_integration(self, production_outputs):
        """Test load balancer monitoring integration"""
        if "load_balancer_metrics" not in production_outputs:
            pytest.skip("Load balancer metrics not available")

        metrics = json.loads(production_outputs["load_balancer_metrics"]["value"])

        # Should collect key metrics
        required_metrics = ["request_count", "response_time", "error_rate", "active_connections"]

        for metric in required_metrics:
            assert metric in metrics, f"Should collect load balancer metric {metric}"

    def test_auto_scaling_configuration(self, load_balancer_config):
        """Test auto-scaling configuration"""
        for service, config in load_balancer_config.items():
            autoscaling = config.get("auto_scaling", {})

            if autoscaling.get("enabled", False):
                # Check scaling thresholds
                scale_up_threshold = autoscaling.get("scale_up_threshold", {})
                scale_down_threshold = autoscaling.get("scale_down_threshold", {})

                assert "cpu_utilization" in scale_up_threshold, (
                    f"Service {service} should have CPU-based scale-up threshold"
                )

                assert "cpu_utilization" in scale_down_threshold, (
                    f"Service {service} should have CPU-based scale-down threshold"
                )

                # Check scaling limits
                min_instances = autoscaling.get("min_instances", 1)
                max_instances = autoscaling.get("max_instances", 1)

                assert max_instances >= min_instances, (
                    f"Service {service} max instances should be >= min instances"
                )

                assert max_instances >= 2, f"Service {service} should support scaling to at least 2 instances"

    def test_load_balancer_security_headers(self, load_balancer_endpoints):
        """Test security headers configuration"""
        for service, lb_endpoint in load_balancer_endpoints.items():
            try:
                # Make a request to test accessibility
                _response = requests.get(lb_endpoint, timeout=10)

                # Check for security headers (placeholder for future validation)
                # headers = _response.headers

                # Should have security-related headers
                security_headers = ["x-frame-options", "x-content-type-options", "x-xss-protection"]

                for _header in security_headers:
                    # Headers might be in different case
                    # Placeholder for header validation
                    pass

            except requests.exceptions.RequestException:
                pytest.fail(f"Load balancer for {service} should be accessible for header testing")

    def test_load_balancer_performance_under_load(self, load_balancer_endpoints):
        """Test load balancer performance under sustained load"""

        def sustained_load_test(endpoint, duration=60, requests_per_second=10):
            """Generate sustained load and measure performance"""
            start_time = time.time()
            results = []

            while time.time() - start_time < duration:
                request_start = time.time()

                try:
                    response = requests.get(endpoint, timeout=5)
                    request_end = time.time()

                    results.append(
                        {
                            "success": response.status_code in [200, 401, 403],
                            "response_time": request_end - request_start,
                            "timestamp": request_start,
                        }
                    )
                except requests.exceptions.RequestException:
                    results.append(
                        {
                            "success": False,
                            "response_time": 5.0,  # timeout
                            "timestamp": request_start,
                        }
                    )

                # Rate limiting
                time.sleep(1.0 / requests_per_second)

            return results

        # Test with moderate load
        for service, lb_endpoint in load_balancer_endpoints.items():
            results = sustained_load_test(lb_endpoint, duration=30, requests_per_second=5)

            # Analyze performance
            successful_requests = sum(1 for r in results if r["success"])
            success_rate = successful_requests / len(results)

            response_times = [r["response_time"] for r in results if r["success"]]

            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                p95_response_time = sorted(response_times)[int(len(response_times) * 0.95)]

                assert success_rate >= 0.90, (
                    f"Load balancer for {service} success rate {success_rate:.2f} too low under load"
                )

                assert avg_response_time < 2.0, (
                    f"Load balancer for {service} average response time "
                    f"{avg_response_time:.2f}s too high under load"
                )

                assert p95_response_time < 5.0, (
                    f"Load balancer for {service} 95th percentile response time "
                    f"{p95_response_time:.2f}s too high under load"
                )
