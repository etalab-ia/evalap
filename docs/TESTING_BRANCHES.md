# Testing Branches Locally - Quick Start

## One-Command Setup

Non-technical users can test any branch with a single command:

```bash
just test-branch
```

This command will:
1. **Show available branches** and let you choose one
2. **Check out the branch** (or update it if already checked out)
3. **Run database migrations** automatically
4. **Start EvalAP** with all services running

That's it! No other steps needed.

## What You Need

1. **Git UI** (optional but recommended for easier branch switching)
   - [GitHub Desktop](https://desktop.github.com/) - Easiest for beginners
   - [GitKraken](https://www.gitkraken.com/) - More features
   - Or use the command line (see below)

2. **Docker Desktop** - For running the application
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

### "Command not found: just"

Install `just`:
- **Mac**: `brew install just`
- **Windows**: Download from [just releases](https://github.com/casey/just/releases)
- **Linux**: `sudo apt install just`

### "Command not found: docker"

Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and restart your terminal.

### Port already in use

Another app is using port 8000 or 8501. Stop that app or wait a moment and try again.

### Need help?

Contact the development team with:
- The branch name you were testing
- The error message from the terminal
- Your operating system
