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
    return
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
    URL="https://api.anthropic.com/v1"
    API_KEY=$ANTHROPIC_API_KEY
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
  #!/usr/bin/env python
  # Does not work !
  import sys, os; sys.path.append("{{work_dir}}")
  from evalap.api.config import DATABASE_URI

  DB_NAME = "{{db_name}}"
  PGURI = DATABASE_URI.replace("+psycopg2", "")
  command = f'psql {PGURI} -c "DROP DATABASE {DB_NAME} WITH (FORCE);"'
  os.system(command)

[no-cd]
drop-table table_name:
  #!/usr/bin/env python
  import sys, os; sys.path.append("{{work_dir}}")
  from evalap.api.config import DATABASE_URI

  TABLE_NAME = "{{table_name}}"
  PGURI = DATABASE_URI.replace("+psycopg2", "")
  command = f'psql "{PGURI}" -c "DROP TABLE IF EXISTS {TABLE_NAME};"'
  exit_status = os.system(command)

[no-cd]
reset-experiment-status *expids:
  #!/usr/bin/env python
  import sys, os; sys.path.append("{{work_dir}}")
  from evalap.api.config import DATABASE_URI

  PGURI = DATABASE_URI.replace("+psycopg2", "")
  expids = "{{expids}}".split()
  req = f"""
    UPDATE experiments
    SET experiment_status = 'finished'
    WHERE id IN ({", ".join(expids)});
  """.strip().replace("\n", " ")
  command = f'psql "{PGURI}" -c "{req}"'
  exit_status = os.system(command)

[no-cd]
get-experiment expid:
  #!/usr/bin/env python
  import sys, os; sys.path.append("{{work_dir}}")
  from evalap.api.config import DATABASE_URI

  PGURI = DATABASE_URI.replace("+psycopg2", "")
  expid = "{{expid}}"
  req = f"""
    SELECT json_agg(row_to_json(t)) FROM (
      SELECT *
      FROM experiments
      WHERE id = {expid}
    ) t;
  """.strip()
  command = f'psql "{PGURI}" -t -P pager=off -c "{req}" | jq'
  exit_status = os.system(command)

rainfrog:
  rainfrog --url postgres://postgres:changeme@localhost:5432/evalap_dev

# Run EvalAP locally or with Docker Compose
# Usage: just run [local|docker]
# - local (default): Run API, runner, and streamlit in parallel with hot reloading
# - docker: Run with Docker Compose (includes hot reloading for all services)
# Access: API http://localhost:8000 | Docs http://localhost:8000/docs | Streamlit http://localhost:8501
run mode="local" log_level="INFO":
  #!/usr/bin/env bash
  if [ "{{mode}}" = "docker" ]; then
    docker compose -f compose.dev.yml up --build
  elif [ "{{mode}}" = "local" ]; then
    # Color codes
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    YELLOW='\033[1;33m'
    PURPLE='\033[0;35m'
    CYAN='\033[0;36m'
    NC='\033[0m' # No Color

    echo -e "${GREEN}Starting evalap services...${NC}"

    # Run database seeding
    echo -e "${PURPLE}Seeding database with initial datasets...${NC}"
    uv run python -m evalap.scripts.run_seed_data

    echo -e "${BLUE}API: http://localhost:8000${NC}"
    echo -e "${CYAN}Streamlit: http://localhost:8501${NC}"
    echo -e "${YELLOW}Runner: starting with LOG_LEVEL={{log_level}}${NC}"
    echo -e "${GREEN}Press Ctrl-C to stop all services${NC}"

    # Function to cleanup background processes
    cleanup() {
      echo -e "\n${RED}Shutting down services...${NC}"
      kill $API_PID $RUNNER_PID $STREAMLIT_PID 2>/dev/null || true
      wait
      echo -e "${GREEN}All services stopped${NC}"
      exit 0
    }

    # Set trap for Ctrl-C
    trap cleanup SIGINT SIGTERM

    # Start API in background with blue prefix
    {
      uv run uvicorn evalap.api.main:app --reload 2>&1 | sed $'s/^/\033[0;34m[API]\033[0m /'
    } &
    API_PID=$!

    # Start runner in background with yellow prefix
    {
      LOG_LEVEL="{{log_level}}" PYTHONPATH="." uv run python -m evalap.runners 2>&1 | sed $'s/^/\033[1;33m[RUNNER]\033[0m /'
    } &
    RUNNER_PID=$!

    # Start streamlit in background with cyan prefix
    {
      uv run streamlit run evalap/ui/demo_streamlit/app.py --server.runOnSave true --server.headless=true 2>&1 | sed $'s/^/\033[0;36m[STREAMLIT]\033[0m /'
    } &
    STREAMLIT_PID=$!

    # Wait for all processes
    wait $API_PID $RUNNER_PID $STREAMLIT_PID
  else
    echo "Invalid mode: {{mode}}. Use 'local' or 'docker'."
    exit 1
  fi

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

#
# Pulumi Infrastructure Commands
#

pulumi *args:
  #!/usr/bin/env bash
  cd infra
  uv run --env-file ../.env pulumi {{args}}

#
# Pulumi State Backend Management
#

state-login stack="dev":
  #!/usr/bin/env bash
  cd infra
  echo "Logging into Pulumi backend for stack: {{stack}}"
  uv run --env-file ../.env pulumi --stack select {{stack}}
  uv run --env-file ../.env pulumi --login 's3://evalap-pulumi-state?endpoint=s3.fr-par.scw.cloud&region=fr-par&s3ForcePathStyle=true'

state-logout:
  #!/usr/bin/env bash
  cd infra
  echo "Logging out of Pulumi backend..."
  uv run --env-file ../.env pulumi logout

state-export file stack="dev":
  #!/usr/bin/env bash
  cd infra
  echo "Exporting state for stack: {{stack}} to {{file}}"
  uv run --env-file ../.env pulumi stack export --stack {{stack}} --file {{file}}

state-import file stack="dev":
  #!/usr/bin/env bash
  cd infra
  echo "Importing state for stack: {{stack}} from {{file}}"
  uv run --env-file ../.env pulumi stack import --stack {{stack}} --file {{file}}

state-list:
  #!/usr/bin/env bash
  cd infra
  echo "Listing all Pulumi stacks..."
  uv run --env-file ../.env pulumi stack ls

state-info stack="dev":
  #!/usr/bin/env bash
  cd infra
  echo "Getting state info for stack: {{stack}}"
  uv run --env-file ../.env pulumi stack select {{stack}}
  uv run --env-file ../.env pulumi stack output

state-refresh stack="dev":
  #!/usr/bin/env bash
  cd infra
  echo "Refreshing state for stack: {{stack}}"
  uv run --env-file ../.env pulumi refresh --stack {{stack}} --yes

state-validate:
  #!/usr/bin/env bash
  echo "Validating state backend configuration..."
  cd infra
  uv run --env-file ../.env python -c "import sys; sys.path.insert(0, '.'); from infra.utils import validation; validation.validate_state_backend_config(bucket_name='evalap-pulumi-state', region='fr-par', endpoint='https://s3.fr-par.scw.cloud'); print('✓ State backend configuration is valid')"
# Test a PR: list open PRs, select one, checkout its branch, migrate, and run
pra:
  #!/usr/bin/env bash
  set -e

  # Check if GitHub CLI is installed
  if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI is not installed"
    echo "📥 Install it from: https://cli.github.com/"
    exit 1
  fi

  echo "📦 Fetching open pull requests..."
  echo ""

  # Get open PRs (not draft, not closed)
  # Using jq instead of template to avoid escaping issues with just
  prs=$(gh pr list --state open --json number,title,headRefName | jq -r '.[] | "\(.number)|\(.title)|\(.headRefName)"')

  if [ -z "$prs" ]; then
    echo "❌ No open pull requests found"
    exit 1
  fi

  # Display PRs and let user choose
  echo "📋 Open Pull Requests:"
  echo ""

  # Create arrays for PR data
  pr_numbers=()
  pr_titles=()
  pr_branches=()
  counter=1

  while IFS='|' read -r number title branch; do
    # Truncate long titles to 60 chars
    if [ ${#title} -gt 60 ]; then
      title="${title:0:57}..."
    fi
    echo "  $counter) #$number - $title"
    pr_numbers+=("$number")
    pr_titles+=("$title")
    pr_branches+=("$branch")
    ((counter++))
  done <<< "$prs"

  echo ""
  read -p "📍 Enter PR number (1-$((counter-1))): " choice

  # Validate choice
  if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt $((counter-1)) ]; then
    echo "❌ Invalid choice"
    exit 1
  fi

  selected_pr=${pr_numbers[$((choice-1))]}
  selected_branch=${pr_branches[$((choice-1))]}

  echo ""
  echo "✅ Selected: PR #$selected_pr - ${pr_titles[$((choice-1))]}"
  echo ""

  # Ask if user wants to clear postgres volume
  echo "❓ Clear PostgreSQL volume? (useful if migrations fail)"
  read -p "   Enter 'yes' to clear, or press Enter to skip: " clear_volume
  if [ "$clear_volume" = "yes" ]; then
    echo "🗑️  Clearing PostgreSQL volume..."
    docker volume rm evalap_postgres_db 2>/dev/null || true
    echo "✅ Volume cleared"
  fi

  echo ""

  # Fetch and checkout branch (fresh copy)
  echo "🔄 Fetching and checking out branch: $selected_branch..."
  git fetch origin "$selected_branch"
  git checkout -B "$selected_branch" "origin/$selected_branch"

  echo ""
  echo "📚 Installing Python dependencies..."
  uv sync --all-extras

  echo ""
  echo "🗄️  Starting PostgreSQL..."
  docker compose -f compose.dev.yml up -d postgres

  echo "⏳ Waiting for PostgreSQL to be ready..."
  for i in {1..30}; do
    if docker compose -f compose.dev.yml exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
      echo "✅ PostgreSQL is ready"
      break
    fi
    if [ $i -eq 30 ]; then
      echo "❌ PostgreSQL failed to start"
      exit 1
    fi
    sleep 1
  done

  # Run migrations and seed data
  echo ""
  echo "🔄 Running database migrations..."
  uv run alembic -c evalap/api/alembic.ini upgrade head

  echo ""
  echo "🌱 Seeding database with initial datasets..."
  uv run python -m evalap.scripts.run_seed_data || true

  echo ""
  echo "🚀 Starting EvalAP services..."
  echo ""

  # Color codes
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  BLUE='\033[0;34m'
  YELLOW='\033[1;33m'
  CYAN='\033[0;36m'
  NC='\033[0m' # No Color

  echo -e "${BLUE}API: http://localhost:8000${NC}"
  echo -e "${CYAN}Streamlit: http://localhost:8501${NC}"
  echo -e "${GREEN}Press Ctrl-C to stop all services${NC}"
  echo ""

  # Function to cleanup background processes
  cleanup() {
    echo -e "\n${RED}Shutting down services...${NC}"
    kill $API_PID $RUNNER_PID $STREAMLIT_PID 2>/dev/null || true
    docker compose -f compose.dev.yml down 2>/dev/null || true
    wait
    echo -e "${GREEN}All services stopped${NC}"
    exit 0
  }

  # Set trap for Ctrl+C
  trap cleanup SIGINT SIGTERM

  # Kill any hanging processes on service ports
  echo "🧹 Cleaning up any hanging processes..."
  lsof -ti:8000 | xargs kill -9 2>/dev/null || true
  lsof -ti:8501 | xargs kill -9 2>/dev/null || true
  lsof -ti:5555 | xargs kill -9 2>/dev/null || true
  lsof -ti:5556 | xargs kill -9 2>/dev/null || true
  sleep 1

  # Start API in background with blue prefix
  {
    uv run uvicorn evalap.api.main:app --reload 2>&1 | sed $'s/^/\033[0;34m[API]\033[0m /'
  } &
  API_PID=$!

  # Start runner in background with yellow prefix
  {
    PYTHONPATH="." uv run python -m evalap.runners 2>&1 | sed $'s/^/\033[1;33m[RUNNER]\033[0m /'
  } &
  RUNNER_PID=$!

  # Start streamlit in background with cyan prefix
  {
    uv run streamlit run evalap/ui/demo_streamlit/app.py --server.runOnSave true --server.headless=true 2>&1 | sed $'s/^/\033[0;36m[STREAMLIT]\033[0m /'
  } &
  STREAMLIT_PID=$!

  # Wait for Uvicorn API to be ready before opening browser
  echo "⏳ Waiting for API to be ready..."
  for i in {1..60}; do
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
      echo "✅ API is ready"
      break
    fi
    if [ $i -eq 60 ]; then
      echo "⚠️  API startup timeout, opening browser anyway..."
      break
    fi
    sleep 1
  done

  echo "🌐 Opening Streamlit UI in browser..."
  if command -v open &> /dev/null; then
    # macOS
    open http://localhost:8501
  elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:8501
  elif command -v start &> /dev/null; then
    # Windows
    start http://localhost:8501
  fi

  # Wait for all processes
  wait $API_PID $RUNNER_PID $STREAMLIT_PID
