#!/usr/bin/env python3
"""Test runner script for the route optimization service."""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run unit tests for the route optimization service")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Run with verbose output"
    )
    # No slow/coverage/lint/type-check in unit-only mode
    
    args = parser.parse_args()
    
    # Base pytest command
    pytest_cmd = ["python", "-m", "pytest"]
    
    if args.verbose:
        pytest_cmd.append("-v")
    
    # Unit tests only
    
    success = True
    
    print("Running unit tests...")
    unit_cmd = pytest_cmd + ["tests/unit/"]
    success &= run_command(unit_cmd, "Unit Tests")
    
    if success:
        print("\n" + "="*60)
        print("✅ All tests passed successfully!")
        print("="*60)
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("❌ Some tests failed!")
        print("="*60)
        sys.exit(1)


if __name__ == "__main__":
    main()
