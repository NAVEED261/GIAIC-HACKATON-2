#!/usr/bin/env python
"""
Database Migration Helper Script

Provides convenient commands to manage database migrations without
needing to remember Alembic CLI syntax.

Usage:
    python migrate.py upgrade       # Apply all pending migrations
    python migrate.py downgrade     # Revert to previous version
    python migrate.py current       # Show current schema version
    python migrate.py history       # Show all migrations
    python migrate.py revision -m "Description"  # Create new migration
"""

import os
import sys
import subprocess
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
os.chdir(backend_dir)


def run_alembic_command(*args):
    """Execute Alembic command and return output."""
    cmd = ["alembic"] + list(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
        return result.returncode
    except FileNotFoundError:
        print("Error: Alembic not found. Install with: pip install alembic sqlmodel")
        return 1


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    commands = {
        "upgrade": ["upgrade", "head"],
        "downgrade": ["downgrade", "-1"],
        "current": ["current"],
        "history": ["history"],
        "revision": ["revision"],
    }

    if command in commands:
        exit_code = run_alembic_command(*commands[command], *args)
        sys.exit(exit_code)
    elif command == "help":
        print(__doc__)
        sys.exit(0)
    else:
        # Pass through to alembic directly
        exit_code = run_alembic_command(command, *args)
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
