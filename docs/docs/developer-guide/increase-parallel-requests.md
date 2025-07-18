---
sidebar_position: 2
---

# Increase the Number of Parallel Requests

This guide will show you how to configure Evalap to handle more parallel requests, which can significantly speed up evaluation experiments.

## Understanding Parallel Processing in Evalap

Evalap can send multiple requests to models simultaneously, which is especially useful when evaluating large datasets. By default, Evalap uses a conservative number of parallel requests to avoid overwhelming the models or your system resources.

## How Parallelism Works in Evalap

Evalap uses ZeroMQ (ZMQ) for task distribution and a thread pool for parallel processing. Here's how it works:

1. The main process receives evaluation tasks and distributes them to worker threads
2. A fixed pool of 8 worker threads processes these tasks concurrently
3. Each worker thread handles one task at a time, allowing up to 8 tasks to be processed simultaneously

This architecture is implemented in the runner component, which creates the worker threads and manages the message queue.

## Modifying Concurrency Settings

The current concurrency level is set to 8 parallel tasks by the `MAX_CONCURRENT_TASKS` constant in `evalap/api/config.py`. To modify this setting:

1. Open the `evalap/api/config.py` file
2. Locate and change the `MAX_CONCURRENT_TASKS = 8` line
3. Restart the Evalap service for changes to take effect

When increasing this value, consider your system's available CPU cores and memory, as well as any rate limits imposed by the model APIs you're using.

## Determining Optimal Parallelism

The optimal number of parallel requests depends on several factors:

1. **System Resources**: Your server's CPU cores and memory will limit effective parallelism
2. **Model API Capacity**: Check your model provider's documentation for rate limits
3. **Network Bandwidth**: Higher parallelism requires more bandwidth
4. **Response Time**: Models with longer inference times benefit more from parallelism


## Monitoring and Troubleshooting

### Signs of Too Much Parallelism

- Increased error rates from model APIs
- Timeouts or connection errors
- System resource exhaustion
- Throttling messages from the API provider

