## Project Architecture

The stack is based on Fastapi+pydantic+sqlachemy for the API in conjonction with ZeroMQ for the Runner.
The project includes an UI/UX based on Streamlit [WIP].


```
evalap/
├── justfile    --> just is a handy way to save and run project-specific commands. See https://just.systems
├── evalap/        --> The evalap code source
│   ├── api/        --> The evaluation API source code
│   ├── runner/     --> The runner (message passing) source code
│   ├── mcp/        --> The MCP client.
│   └── ui/         --> [WIP] The user interface code source
├── tests/      --> The tests
└── notebooks/  --> Example and demo notebooks
```

## Environment

The project needs the following API key to be set perform LLM based metrics: 

```bash
export OPENAI_API_KEY="You secret key"
```

All the project global settings and environmant variables are handled in `evalap/api/config.py`.

The environement variables can also be defined in a `.env` file at the root of the project.


## Database initialization 

1. Launch the development services:
```
    docker-compose -f compose.dev.yml up
```

2. Create the first migration script:
```
    alembic -c evalap/api/alembic.ini revision --autogenerate -m "Table Initialization"
```

3. Initialize/Update the database schema:
```
    alembic -c evalap/api/alembic.ini upgrade head
```
4. If you modify the schema :
```
    alembic -c evalap/api/alembic.ini revision --autogenerate -m "text explication"
    alembic -c evalap/api/alembic.ini upgrade head  
```

## Run API

1. Install the requirements (in .venv if you prefer)
```
    pip install .
```
2. Launch the API:
```
    uvicorn evalap.api.main:app --reload
```
3. Launch the runner:
```
    PYTHONPATH="." python -m evalap.runners
    # To change the default loggin level you can do:
    #LOG_LEVEL="DEBUG" PYTHONPATH="." python -m evalap.runners
```

## Swagger

Access the API documentation at: http://localhost:8000/redoc (or http://localhost:8000/docs if you prefer the legacy version).


## Streamlit Application

To run the streamlit frontend, run : 

    streamlit run evalap/ui/demo_streamlit/app.py --server.runOnSave true


## Jupyter Tutorial

The `notebook/` directory contains examples of API usage.


## Adding new metrics

Each single metric should be defined in a file in `evalap/api/metrics/{metric_name}.py`.
The file should be self-contained, i.e contains the eventual prompt and settings related to the metric.
The metric should be decorated as followinf example to be registed as a known metric of EVALAP: 


```python
from . import metric_registry

@metric_registry.register(
    name="metric_name", # the name that identified the metric
    description="Explain the metrics briefly"
    metric_type="llm",  # to be documented, not yet used
    require=["output", "output_true", "query"] # the fields that should be present in the dataset related to experiment under evaluation
)
def metric_name_metric(output:str, output_true:str, **kwargs) -> float:
    # ...
    # ...You code goes here
    # ...
    return score
    # or, if you want to store the intermediate generated observation by the metric (like a judge answer typically)
    #return score, observation
```


## Unit Tests

Tests can be found in api/tests.
To run unit tests, use : 

    pytest


## Install python package

    python -m pip install build twine
    twine upload dist/*

## use ruff 
```
 ruff format --config=pyproject.toml file_path
```
