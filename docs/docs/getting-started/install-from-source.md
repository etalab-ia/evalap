---
sidebar_position: 1
---

# Install from Source

This guide will walk you through the process of installing Evalap from source code.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Clone the Repository

```bash
git clone https://github.com/etalab/evalap.git
cd evalap
```

## Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
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

## Run the Application

```bash
python -m evalap.main
```

The application should now be running at `http://localhost:8000`.

## Verify Installation

To verify that Evalap is running correctly, open your web browser and navigate to:

```
http://localhost:8000/docs
```

You should see the API documentation page.

## Next Steps

Now that you have Evalap installed, you can:

- [Install with Docker](./install-with-docker.md) for an alternative installation method
- [Add your dataset](../user-guides/add-your-dataset.md) to start evaluating models
- [Create a simple experiment](../user-guides/create-a-simple-experiment.md) to test the platform