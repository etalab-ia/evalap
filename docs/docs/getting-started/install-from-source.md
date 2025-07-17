sidebar_position: 2

# Install from Source

This guide will walk you through the process of installing Evalap from source code. Installing from source is recommended for developers who want to contribute to the project or need the latest features that may not be available in the released versions.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.10 or higher
- pip (Python package installer)
- Git

## Clone the Repository

```bash
git clone https://github.com/etalab-ia/evalap.git
cd evalap
```

## Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

## Install Dependencies

```bash
pip install .
```

## Configure the Application

To protect the API sensitive request such as deleting experiment or dataset you can set an admin token

```bash
export ADMIN_TOKEN="Your evalap admin token"
```

You can access LLM models from major providers by setting up your API keys if you have accounts with:

```bash
export OPENAI_API_KEY="Your secret key"
export ANTHROPIC_API_KEY="Your secret key"
export MISTRAL_API_KEY="Your secret key"
export ALBERT_API_KEY="Your secret key"
```

You can also define environment variables in a `.env` file at the root of the project.

All project global settings and environment variables are handled in `evalap/api/config.py`.

## Database Initialization

1. Launch the development services:

```bash
docker compose -f compose.dev.yml up
```

2. Create the first migration script:

```bash
alembic -c evalap/api/alembic.ini revision --autogenerate -m "Table Initialization"
```

3. Initialize/Update the database schema:

```bash
alembic -c evalap/api/alembic.ini upgrade head
```


## Run the Application

```bash
# Step 1: Run the API server
uvicorn evalap.api.main:app --reload --host 0.0.0.0 --port 8000

# Step 2: In a separate terminal, activate your virtual environment if needed, then run the runner
PYTHONPATH="." python -m evalap.runners
```

### Logging Configuration

You can adjust the logging level for more detailed output:

```bash
# Run with debug logging enabled
LOG_LEVEL="DEBUG" PYTHONPATH="." python -m evalap.runners
```

### Troubleshooting

If you encounter issues starting the application:

1. Ensure all dependencies are correctly installed
2. Verify that the database is running (check Docker containers)
3. Check that environment variables are properly set
4. Look for error messages in the terminal output

The API should now be running at `http://localhost:8000`.

## Run the Streamlit Frontend (Optional)

```bash
streamlit run evalap/ui/demo_streamlit/app.py --server.runOnSave true
```

## Verify Installation

To verify that Evalap is running correctly, open your web browser and navigate to:

```
http://localhost:8000/redoc
```

You should see the API documentation page. You can also use `http://localhost:8000/docs` if you prefer the swagger version.

## Next Steps

Now that you have Evalap installed, you can:

- Explore the Jupyter notebook examples in the `notebooks/` directory
- [Install with Docker](./install-with-docker.md) for an alternative installation method
- [Add your dataset](../user-guides/add-your-dataset.md) to start evaluating models
- [Create a simple experiment](../user-guides/create-a-simple-experiment.md) to test the platform
