## Code Architecture
|- eg1
|-- api
|-- contrib
|-- notebook


1. **api** contains the evaluation API.
2. **contrib** contains the docker-compose files.
3. **notebook** contains example notebooks.




## Database initialization 

1. Launch the development services:
```
    docker-compose -f contrib/docker-compose.dev.yml up
```

2. Create the first migration script:
```
    alembic -c api/alembic.ini revision --autogenerate -m "Table Initialization"
```

3. Initialize/Update the database schema:
```
    alembic -c api/alembic.ini upgrade head
```


## Run API


1. Install the requirements (in .venv if you prefer)
```
    pip install .
```
2. Launch the API:
```
    uvicorn api.main:app --reload
```
3. Launch the runner:
```
    PYTHONPATH="." python -m api.runners
    # To change the default loggin level you can do:
    #LOG_LEVEL="DEBUG" PYTHONPATH="." python -m api.runners
```

## Swagger

Access the API documentation at: http://localhost:8000/redoc.

## Streamlit Application (not available)

Once the Docker containers are launched, you can access the Streamlit application at: http://localhost:8501


## Jupyter Tutorial

The `notebook/` directory contains examples of API usage.


## Adding new metrics

Each single metric should be defined in a file in `api/metrics/{metric_name}.py`.
The file should be self-contained, i.e contains the eventual prompt and settings related to the metric.
The metric should be decorated as followinf example to be registed as a known metric of EG1: 


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
In development
