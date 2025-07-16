---
sidebar_position: 2
---

# Install with Docker

This guide will walk you through the process of installing and running Evalap using Docker.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose (optional, but recommended)
- Git

## Clone the Repository

```bash
git clone https://github.com/etalab/evalap.git
cd evalap
```

## Configure the Application

1. Create a configuration file by copying the example:

```bash
cp config.example.yaml config.yaml
```

2. Edit the configuration file to match your environment:

```bash
# Use your favorite text editor
nano config.yaml
```

## Using Docker Compose (Recommended)

1. Build and start the containers:

```bash
docker-compose up -d
```

2. The application should now be running at `http://localhost:8000`.

## Using Docker Directly

1. Build the Docker image:

```bash
docker build -t evalap .
```

2. Run the container:

```bash
docker run -p 8000:8000 -v $(pwd)/config.yaml:/app/config.yaml evalap
```

## Verify Installation

To verify that Evalap is running correctly, open your web browser and navigate to:

```
http://localhost:8000/docs
```

You should see the API documentation page.

## Next Steps

Now that you have Evalap installed with Docker, you can:

- [Add your dataset](../user-guides/add-your-dataset.md) to start evaluating models
- [Create a simple experiment](../user-guides/create-a-simple-experiment.md) to test the platform