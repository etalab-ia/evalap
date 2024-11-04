## Run test API

1. Launch the API:

    uvicorn api.main:app --reload

2. Launch the runner:

    PYTHONPATH="." python -m api.runners


## Adding new metrics

WIP


## Database initialization

Launch the development services:

    docker-compose -f contrib/docker-compose.test.yml up


Create the first migration script:

    alembic revision --autogenerate -m "Table Initialization"


Initialize the database:

    alembic upgrade head

