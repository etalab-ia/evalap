# Testing Branches Locally - Quick Start

## One-Command Setup

### Option A: Test a Pull Request (Recommended)

```bash
just test-pr
```

This command will:
1. **List all open pull requests** (excluding drafts and closed)
2. **Let you select one** by number
3. **Check out the PR's branch** automatically
4. **Run database migrations**
5. **Start EvalAP** with all services running

### Option B: Test a Branch

```bash
just test-branch
```

This command will:
1. **Show available branches** and let you choose one
2. **Check out the branch** (or update it if already checked out)
3. **Run database migrations** automatically
4. **Start EvalAP** with all services running

Both commands are interactive and handle all setup automatically.

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

### Option 1: Using GitHub Desktop (Easiest)

1. **Install** [GitHub Desktop](https://desktop.github.com/)
2. **Open GitHub Desktop** and clone/open the EvalAP repository
3. **Switch to your desired branch** using the branch dropdown in GitHub Desktop
4. **Open Terminal** in the project folder (GitHub Desktop → Repository → Open in Terminal)
5. **Run the command**:
   ```bash
   just test-branch
   ```

### Option 2: Using Command Line

1. **Open Terminal/Command Prompt** in the project folder
2. **Run**:
   ```bash
   just test-branch
   ```
3. **Select a branch** from the interactive menu

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

There are no open PRs at the moment. Use `just test-branch` instead to test any branch.

### Need help?

Contact the development team with:
- The branch or PR number you were testing
- The error message from the terminal
- Your operating system
