#!/usr/bin/env bash

MODE="${1:-local}"
LOG_LEVEL="${2:-INFO}"

if [ "$MODE" = "docker" ]; then
  docker compose -f compose.dev.yml up --build
elif [ "$MODE" = "local" ]; then
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
  echo -e "${YELLOW}Runner: starting with LOG_LEVEL=${LOG_LEVEL}${NC}"
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
    LOG_LEVEL="${LOG_LEVEL}" PYTHONPATH="." uv run python -m evalap.runners 2>&1 | sed $'s/^/\033[1;33m[RUNNER]\033[0m /'
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
  echo "Invalid mode: ${MODE}. Use 'local' or 'docker'."
  exit 1
fi
