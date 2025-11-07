# Acceptance Testing - Quick Start

Test pull requests locally before they're merged. This guide is for non-technical users who want to validate features in a real environment.

## One-Command Setup

```bash
just test-pr
```

This command will:
1. **List all open pull requests** (excluding drafts and closed)
2. **Let you select one** by number
3. **Check out the PR's branch** automatically
4. **Run database migrations**
5. **Start EvalAP** with all services running

That's it! No other steps needed.

## What You Need

1. **GitHub CLI** (required for `just test-pr`)
   - [Download GitHub CLI](https://cli.github.com/)
   - Verify: Open Terminal and type `gh --version`

2. **jq** (required for `just test-pr` - JSON processor)
   - **Mac**: `brew install jq`
   - **Windows**: Download from [stedolan.github.io/jq](https://stedolan.github.io/jq/download/)
   - **Linux**: `sudo apt install jq` (Debian/Ubuntu)
   - Verify: Open Terminal and type `jq --version`

3. **Git UI** (optional but recommended for easier branch switching)
   - [GitHub Desktop](https://desktop.github.com/) - Easiest for beginners
   - [GitKraken](https://www.gitkraken.com/) - More features
   - Or use the command line (see below)

4. **Docker Desktop** - For running the application
   - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)

## How to Use

1. **Open Terminal/Command Prompt** in the project folder
2. **Run**:
   ```bash
   just test-pr
   ```
3. **Select a PR** from the interactive menu by entering its number
4. **Optionally clear the PostgreSQL volume** if you want a fresh database
5. Done! The application will start automatically

## Access the Application

Once running, open your browser:

- **Main UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

## Stop the Application

Press `Ctrl + C` in the terminal.

## Troubleshooting

### "Command not found: gh" (for `just test-pr`)

Install GitHub CLI:
- **Mac**: `brew install gh`
- **Windows**: Download from [cli.github.com](https://cli.github.com/)
- **Linux**: Follow [installation guide](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)

Then authenticate:
```bash
gh auth login
```

### "Command not found: jq" (for `just test-pr`)

Install jq:
- **Mac**: `brew install jq`
- **Windows**: Download from [stedolan.github.io/jq](https://stedolan.github.io/jq/download/)
- **Linux**: `sudo apt install jq` (Debian/Ubuntu)

### "Command not found: just"

Install `just`:
- **Mac**: `brew install just`
- **Windows**: Download from [just releases](https://github.com/casey/just/releases)
- **Linux**: `sudo apt install just`

### "Command not found: docker"

Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and restart your terminal.

### Port already in use

Another app is using port 8000 or 8501. Stop that app or wait a moment and try again.

### "No open pull requests found"

There are no open PRs at the moment. Check back later or contact the development team.

### Need help?

Contact the development team with:
- The PR number you were testing
- The error message from the terminal
- Your operating system
