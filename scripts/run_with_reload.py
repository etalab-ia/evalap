#!/usr/bin/env python3
"""
Hot-reload wrapper for the runner process.
Watches for Python file changes and automatically restarts the runner.
"""

import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class RunnerReloader(FileSystemEventHandler):
    """File system event handler that restarts the runner on Python file changes."""

    def __init__(self, command: list[str], watch_path: Path):
        self.command = command
        self.watch_path = watch_path
        self.process = None
        self.restart_pending = False
        self.last_restart = 0
        self.debounce_seconds = 1.0  # Debounce rapid file changes
        self.start_process()

    def start_process(self):
        """Start the runner process."""
        if self.process:
            self.stop_process()

        print(f"[Reloader] Starting: {' '.join(self.command)}")
        self.process = subprocess.Popen(
            self.command,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        self.last_restart = time.time()

    def stop_process(self):
        """Stop the runner process gracefully."""
        if self.process and self.process.poll() is None:
            print("[Reloader] Stopping process...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("[Reloader] Process didn't terminate, killing...")
                self.process.kill()
                self.process.wait()

    def should_reload(self, event):
        """Determine if we should reload based on the file change."""
        # Only reload for Python files
        if not event.src_path.endswith(".py"):
            return False

        # Ignore __pycache__ and other common directories
        path = Path(event.src_path)
        if any(part.startswith(".") or part == "__pycache__" for part in path.parts):
            return False

        # Debounce: don't restart too frequently
        if time.time() - self.last_restart < self.debounce_seconds:
            self.restart_pending = True
            return False

        return True

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        if self.should_reload(event):
            print(f"[Reloader] Detected change in: {event.src_path}")
            self.start_process()

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        if self.should_reload(event):
            print(f"[Reloader] Detected new file: {event.src_path}")
            self.start_process()


def main():
    """Main entry point for the reloader."""
    if len(sys.argv) < 2:
        print("Usage: run_with_reload.py <command> [args...]")
        sys.exit(1)

    # Get the command to run
    command = sys.argv[1:]

    # Determine the watch path (current directory or evalap directory)
    watch_path = Path.cwd()
    evalap_path = watch_path / "evalap"
    if evalap_path.exists():
        watch_path = evalap_path

    print(f"[Reloader] Watching for changes in: {watch_path}")
    print(f"[Reloader] Will run: {' '.join(command)}")

    # Create the event handler and observer
    event_handler = RunnerReloader(command, watch_path)
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)

            # Check if process died unexpectedly
            if event_handler.process.poll() is not None:
                print("[Reloader] Process exited, restarting...")
                event_handler.start_process()

            # Handle pending restarts after debounce period
            if event_handler.restart_pending:
                if time.time() - event_handler.last_restart >= event_handler.debounce_seconds:
                    print("[Reloader] Processing pending restart...")
                    event_handler.restart_pending = False
                    event_handler.start_process()

    except KeyboardInterrupt:
        print("[Reloader] Shutting down...")
        observer.stop()
        event_handler.stop_process()

    observer.join()


if __name__ == "__main__":
    main()
