#!/usr/bin/env python3
"""Pre-commit hook to ensure newly added or modified Git LFS-tracked files.

Do not exceed a configurable size limit.

Usage:
    check_lfs_size.py [--max-size 50]

Default max size is 50 MB.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def get_staged_files() -> list[Path]:
    """Return a list of staged files (added or modified)."""
    try:
        output = subprocess.check_output(
            ["/usr/bin/git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
            text=True,
        )
        return [Path(line.strip()) for line in output.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        return []


def is_tracked_by_lfs(file_path: Path) -> bool:
    """Check if the file is tracked by Git LFS."""
    try:
        output = subprocess.check_output(  # noqa: S603
            ["/usr/bin/git", "check-attr", "filter", str(file_path)], text=True
        )
        return "lfs" in output
    except subprocess.CalledProcessError:
        return False


def get_file_size(file_path: Path) -> int:
    """Return file size in bytes."""
    return file_path.stat().st_size


def bytes_to_mb(num_bytes: int) -> float:
    """Convert bytes to megabytes (2 decimal places)."""
    return round(num_bytes / (1024 * 1024), 2)


def check_lfs_file_sizes(max_size_mb: float) -> int:
    """Check all LFS-tracked staged files against the size limit."""
    staged_files = get_staged_files()
    if not staged_files:
        return 0

    oversized_files = []

    for file in staged_files:
        if file.exists() and is_tracked_by_lfs(file):
            size_bytes = get_file_size(file)
            if size_bytes > max_size_mb * 1024 * 1024:
                oversized_files.append((file, bytes_to_mb(size_bytes)))

    if oversized_files:
        print("Error: The following LFS-tracked files exceed the size limit:")
        for file, size_mb in oversized_files:
            print(f"  {file}: {size_mb} MB (limit: {max_size_mb} MB)")
        return 1

    return 0


def main() -> int:
    """Parse arguments and check LFS file sizes."""
    parser = argparse.ArgumentParser(
        description="Check Git LFS file sizes before commit."
    )
    parser.add_argument(
        "--max-size",
        type=float,
        default=50.0,
        help="Maximum allowed file size in MB (default: 50)",
    )
    args = parser.parse_args()

    return check_lfs_file_sizes(args.max_size)


if __name__ == "__main__":
    sys.exit(main())
