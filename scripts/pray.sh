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

echo ""
echo "⚠️  WARNING: The following operations will:"
echo "   - Remove ALL untracked files and directories (git clean -fd)"
echo "   - Discard ALL local uncommitted changes (git reset --hard)"
echo ""
read -p "   Type 'yes' to continue: " confirm_clean
if [ "$confirm_clean" != "yes" ]; then
  echo "❌ Aborted by user"
  exit 1
fi

git clean -fd  # Remove untracked files and directories
git reset --hard "origin/$selected_branch"  # Reset to match remote exactly

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
echo -e "${CYAN}Docusaurus: http://localhost:3000${NC}"
echo -e "${GREEN}Press Ctrl-C to stop all services${NC}"
echo ""

# Function to cleanup background processes
cleanup() {
  echo -e "\n${RED}Shutting down services...${NC}"
  kill $API_PID $RUNNER_PID $DOCUSAURUS_PID 2>/dev/null || true
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
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
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

# Start Docusaurus in background with cyan prefix
{
  (cd docs && npm run start -- --port 3000) 2>&1 | sed $'s/^/\033[0;36m[DOCUSAURUS]\033[0m /'
} &
DOCUSAURUS_PID=$!

# Wait for Uvicorn API to be ready before opening browser
echo "⏳ Waiting for API to be ready..."
for i in {1..60}; do
  if curl -s http://localhost:8000/api-docs > /dev/null 2>&1; then
    echo "✅ API is ready"
    break
  fi
  if [ $i -eq 60 ]; then
    echo "⚠️  API startup timeout, opening browser anyway..."
    break
  fi
  sleep 1
done

echo "🌐 Opening Docusaurus UI in browser..."
if command -v open &> /dev/null; then
  # macOS
  open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
  # Linux
  xdg-open http://localhost:3000
elif command -v start &> /dev/null; then
  # Windows
  start http://localhost:3000
fi

# Wait for all processes
wait $API_PID $RUNNER_PID $DOCUSAURUS_PID
