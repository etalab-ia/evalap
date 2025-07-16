---
sidebar_position: 2
---

# Increase the Number of Parallel Requests

This guide will show you how to configure Evalap to handle more parallel requests, which can significantly speed up evaluation experiments.

## Understanding Parallel Processing in Evalap

Evalap can send multiple requests to models simultaneously, which is especially useful when evaluating large datasets. By default, Evalap uses a conservative number of parallel requests to avoid overwhelming the models or your system resources.

## Prerequisites

Before increasing parallel requests, ensure you have:

- A properly configured Evalap installation
- Sufficient system resources (CPU, memory, network bandwidth)
- Understanding of your model API's rate limits and capacity

## Configuration Methods

You can increase parallel requests in several ways:

### Method 1: Configuration File

Edit the `config.yaml` file to set the default parallel requests for all experiments:

```yaml
experiment:
  default_parallel_requests: 10  # Increase this number as needed
  max_parallel_requests: 50      # Maximum allowed parallel requests
```

### Method 2: Environment Variables

Set environment variables to override the configuration file:

```bash
export EVALAP_DEFAULT_PARALLEL_REQUESTS=10
export EVALAP_MAX_PARALLEL_REQUESTS=50
```

For Docker installations:

```bash
docker run -p 8000:8000 \
  -e EVALAP_DEFAULT_PARALLEL_REQUESTS=10 \
  -e EVALAP_MAX_PARALLEL_REQUESTS=50 \
  -v $(pwd)/config.yaml:/app/config.yaml evalap
```

### Method 3: Per-Experiment Configuration

When creating an experiment via the API or web interface, you can specify the number of parallel requests for that specific experiment:

```python
# API example
experiment_config = {
    "name": "High Parallelism Experiment",
    "description": "Testing with high parallelism",
    "datasets": ["dataset_id_1"],
    "models": ["model_id_1", "model_id_2"],
    "metrics": ["accuracy", "f1_score"],
    "parameters": {
        "max_parallel_requests": 20  # Set parallel requests for this experiment
    }
}
```

In the web interface, you can set this value in the "Advanced Settings" section when creating or editing an experiment.

## Determining Optimal Parallelism

The optimal number of parallel requests depends on several factors:

1. **Model API Capacity**: Check your model provider's documentation for rate limits
2. **System Resources**: Monitor CPU, memory, and network usage during experiments
3. **Network Bandwidth**: Higher parallelism requires more bandwidth
4. **Response Time**: Models with longer inference times benefit more from parallelism

### Benchmarking

To find the optimal setting, run a series of small experiments with increasing parallelism and measure the total execution time:

```python
import time
import requests

API_URL = "https://evalap.etalab.gouv.fr/api"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY"}

# Base experiment configuration
base_config = {
    "name": "Parallelism Benchmark",
    "datasets": ["dataset_id_1"],
    "models": ["model_id_1"],
    "metrics": ["accuracy"],
    "parameters": {"sample_size": 100}
}

results = []

# Test different parallelism settings
for parallel_requests in [1, 5, 10, 20, 50]:
    # Update configuration
    config = base_config.copy()
    config["name"] = f"Benchmark - {parallel_requests} Parallel"
    config["parameters"]["max_parallel_requests"] = parallel_requests
    
    # Create experiment
    response = requests.post(
        f"{API_URL}/experiments",
        headers=HEADERS,
        json=config
    )
    experiment_id = response.json()["id"]
    
    # Run experiment and measure time
    start_time = time.time()
    requests.post(
        f"{API_URL}/experiments/{experiment_id}/run",
        headers=HEADERS
    )
    
    # Wait for completion
    while True:
        status_response = requests.get(
            f"{API_URL}/experiments/{experiment_id}/status",
            headers=HEADERS
        )
        status = status_response.json()["status"]
        if status in ["completed", "failed"]:
            break
        time.sleep(5)
    
    end_time = time.time()
    duration = end_time - start_time
    
    results.append({
        "parallel_requests": parallel_requests,
        "duration": duration,
        "status": status
    })
    
    print(f"Parallelism: {parallel_requests}, Duration: {duration:.2f}s, Status: {status}")

# Find optimal setting
valid_results = [r for r in results if r["status"] == "completed"]
if valid_results:
    optimal = min(valid_results, key=lambda x: x["duration"])
    print(f"\nOptimal parallelism: {optimal['parallel_requests']} (Duration: {optimal['duration']:.2f}s)")
```

## Monitoring and Troubleshooting

### Signs of Too Much Parallelism

- Increased error rates from model APIs
- Timeouts or connection errors
- System resource exhaustion
- Throttling messages from the API provider

### Logging and Monitoring

Enable detailed logging to monitor request performance:

```yaml
# In config.yaml
logging:
  level: DEBUG
  request_logging: true
```

Check the logs for patterns of errors or slowdowns that might indicate parallelism issues.

## Conclusion

Increasing parallel requests can significantly improve the performance of your evaluation experiments. Start with conservative values and gradually increase based on your system's capabilities and the model API's limits. Monitor performance and errors to find the optimal balance between speed and reliability.