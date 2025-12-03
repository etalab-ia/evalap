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
  #!/usr/bin/env sh
  if [ "{{provider}}" = "albert" ]; then
    URL="https://albert.api.etalab.gouv.fr/v1"
    API_KEY=$ALBERT_API_KEY
  elif [ "{{provider}}" = "albert-staging" ]; then
    URL="https://albert.api.staging.etalab.gouv.fr/v1"
    API_KEY=$ALBERT_API_KEY_STAGING
  elif [ "{{provider}}" = "albert-dev" ]; then
    URL="https://albert.api.dev.etalab.gouv.fr/v1"
    API_KEY=$ALBERT_API_KEY_DEV
  elif [ "{{provider}}" = "anthropic" ]; then
    URL="https://api.anthropic.com/v1"
    API_KEY=$ANTHROPIC_API_KEY
    curl -XGET -H "x-api-key: $API_KEY" -H "anthropic-version: 2023-06-01" $URL/models | jq '[.data.[] | {id, type, owned_by, aliases}]'
    exit 0
  elif [ "{{provider}}" = "openai" ]; then
    URL="https://api.openai.com/v1"
    API_KEY=$OPENAI_API_KEY
  elif [ "{{provider}}" = "mistral" ]; then
    URL="https://api.mistral.ai/v1"
    API_KEY=$MISTRAL_API_KEY
  elif [ "{{provider}}" = "xai" ]; then
    URL="https://api.x.ai/v1"
    API_KEY=$XAI_API_KEY
  elif [ "{{provider}}" = "mammouth" ]; then
    URL="https://api.mammouth.ai/v1"
    API_KEY=$MAMMOUTH_API_KEY
  fi

  curl -XGET -H "Authorization: Bearer $API_KEY" $URL/models | jq '[.data.[] | {id, type, owned_by, aliases}]'

chat-completion model="mistralai/Mistral-Small-3.2-24B-Instruct-2506" provider="albert":
  #!/usr/bin/env sh
  if [ "{{provider}}" = "albert" ]; then
    URL="https://albert.api.etalab.gouv.fr/v1"
    API_KEY=$ALBERT_API_KEY
  elif [ "{{provider}}" = "albert-staging" ]; then
    URL="https://albert.api.staging.etalab.gouv.fr/v1"
    API_KEY=$ALBERT_API_KEY_STAGING
  elif [ "{{provider}}" = "openai" ]; then
    URL="https://api.openai.com/v1"
    API_KEY=$OPENAI_API_KEY
  elif [ "{{provider}}" = "anthropic" ]; then
    URL="https://api.anthropic.com/v1/messages"
    API_KEY=$ANTHROPIC_API_KEY

    curl "$URL" \
        -H "x-api-key: $API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "{{model}}",
          "max_tokens": 1024,
          "messages": [
            {"role": "user", "content": "Combien de fois 'p' dans développer ? Combien font 2*10+50-20 ?"}
          ]
        }'
    exit 0
  elif [ "{{provider}}" = "mistral" ]; then
    URL="https://api.mistral.ai/v1"
    API_KEY=$MISTRAL_API_KEY
  fi

  curl "$URL/chat/completions" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $API_KEY" \
      -d '{
        "model": "{{model}}",
        "messages": [
          {"role": "system", "content": "Answer dramatically and with emojis."},
          {"role": "user", "content": "Combien de fois 'p' dans développer ? Combien font 2*10+50-20 ?"}
        ]
      }'

chat-completion-cortex:
  #!/usr/bin/env bash
  models_and_urls=(
    "https://model1.multivacplatform.org/v1|$CORTEX_API_KEY|meta-llama/Llama-3.2-3B-Instruct"
    "https://model2.multivacplatform.org/v1|$CORTEX_API_KEY|deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
    "https://model4.multivacplatform.org/v1|$CORTEX_API_KEY|meta-llama/Llama-3.3-70B-Instruct"
  )

  for entry in "${models_and_urls[@]}"; do
    IFS='|' read -r url key model <<< "$entry"

    curl "$url/chat/completions" \
         -H "Content-Type: application/json" \
         -H "Authorization: Bearer $key" \
         -d '{
           "model": "'"$model"'",
           "messages": [
             {"role": "system", "content": "Answer dramatically and with emojis."},
             {"role": "user", "content": "Combien de fois 'p' dans développer ? Combien font 2*10+50-20 ?"}
           ]
           }' | jq
    done

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
  #!/usr/bin/env sh
  if [ "{{env}}" = "dev" ]; then
    curl -u elastic:$ELASTICSEARCH_PASSWORD -X GET "$ELASTICSEARCH_URL/_cat/indices?v"
  elif [ "{{env}}" = "staging" ]; then
    curl -u elastic:$ELASTICSEARCH_PASSWORD -X GET "$ELASTICSEARCH_URL/_cat/indices?v"
  elif [ "{{env}}" = "prod" ]; then
    curl -u elastic:$ELASTICSEARCH_PASSWORD -X GET "$ELASTICSEARCH_URL/_cat/indices?v"
  fi

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
