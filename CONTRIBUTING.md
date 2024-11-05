## Run test API

1. Install the requirements

    pip install .

1. Launch the API:

    uvicorn api.main:app --reload

2. Launch the runner:

    PYTHONPATH="." python -m api.runners


## Adding new metrics

WIP


## Database initialization

Launch the development services:

    docker-compose -f contrib/docker-compose.dev.yml up


Create the first migration script:

    alembic -c api/alembic.ini revision --autogenerate -m "Table Initialization"


Initialize/Update the database:

    alembic -c api/alembic.ini upgrade head

