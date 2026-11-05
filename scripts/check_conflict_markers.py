#!/usr/bin/env python3
"""Fail if any tracked text file still contains Git conflict markers.

Usage:
    python scripts/check_conflict_markers.py

A forgotten marker is a classic way to break a build after a merge. This
check runs in CI so it never reaches ``main``.
"""

import re
import subprocess
import sys

MARKER = re.compile(r"^(<{7}( .*)?|={7}|>{7}( .*)?)$")


def find_markers(text: str):
    """Return (line_number, line) pairs for every conflict-marker line."""
    return [
        (number, line)
        for number, line in enumerate(text.splitlines(), start=1)
        if MARKER.match(line)
    ]


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files", "-z"], check=True, capture_output=True, text=True
    ).stdout
    # During a conflict Git lists a file once per merge stage; keep each name once.
    return list(dict.fromkeys(name for name in out.split("\0") if name))


def main() -> int:
    problems = []
    for name in tracked_files():
        try:
            with open(name, encoding="utf-8") as handle:
                text = handle.read()
        except (UnicodeDecodeError, OSError):
            continue  # binary or unreadable: not our concern
        for number, line in find_markers(text):
            problems.append(f"{name}:{number}: {line}")
    if problems:
        print("Unresolved merge-conflict markers found:\n")
        print("\n".join(f"  {p}" for p in problems))
        return 1
    print("OK: no conflict markers in tracked files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
