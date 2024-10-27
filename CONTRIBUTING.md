

## Database initialization

Launch the development services:

    docker-compose -f contrib/docker-compose.test.yml up


Create the first migration script:

    alembic revision --autogenerate -m "Table Initialization"


Initialize the database:

    alembic upgrade head


## Run test API

    uvicorn api.main:app --reload


