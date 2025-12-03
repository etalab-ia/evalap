set quiet
set dotenv-load

work_dir := `pwd`

default:
  just --list

clean:
  rm -rf build/ evalap.egg-info/

#
# Openai API utils
#

list-model provider="albert":
  scripts/list_model.sh {{provider}}

chat-completion model="mistralai/Mistral-Small-3.2-24B-Instruct-2506" provider="albert":
  scripts/chat_completion.sh {{model}} {{provider}}

chat-completion-cortex:
  scripts/chat_completion_cortex.sh

#
# Alembic commands
#

alembic-init:
  uv run alembic -c evalap/api/alembic.ini revision --autogenerate -m "Table Initialization"

alembic-generate-revision name:
  uv run alembic -c evalap/api/alembic.ini upgrade head
  uv run alembic -c evalap/api/alembic.ini revision --autogenerate -m "{{name}}"

alembic-upgrade:
  uv run alembic -c evalap/api/alembic.ini upgrade head

alembic-downgrade hash:
  uv run alembic -c evalap/api/alembic.ini downgrade {{hash}}

alembic-history:
  uv run alembic -c evalap/api/alembic.ini history

#
# Search engine
#

list-indexes env="dev":
  scripts/list_indexes.sh {{env}}

#
# DB Queries
#

seed:
  uv run python -m evalap.scripts.run_seed_data


[no-cd]
drop-database db_name="evalap_dev":
  uv run python scripts/drop_database.py {{db_name}}

[no-cd]
drop-table table_name:
  uv run python scripts/drop_table.py {{table_name}}

[no-cd]
reset-experiment-status *expids:
  uv run python scripts/reset_experiment_status.py {{expids}}

[no-cd]
get-experiment expid:
  uv run python scripts/get_experiment.py {{expid}}

rainfrog:
  rainfrog --url postgres://postgres:changeme@localhost:5432/evalap_dev

# Run EvalAP locally or with Docker Compose
# Usage: just run [local|docker]
# - local (default): Run API, runner, and streamlit in parallel with hot reloading
# - docker: Run with Docker Compose (includes hot reloading for all services)
# Access: API http://localhost:8000 | Docs http://localhost:8000/docs | Streamlit http://localhost:8501
run mode="local" log_level="INFO":
  scripts/run_evalap.sh {{mode}} {{log_level}}

test:
  pytest

publish:
  uv build
  uv publish

format:
  ruff format --config=pyproject.toml .

lint:
  ruff check --config=pyproject.toml --fix .

sync:
  uv sync --all-extras
  uv run pre-commit install

# Test a PR: list open PRs, select one, checkout its branch, migrate, and run
pray:
  scripts/pray.sh
