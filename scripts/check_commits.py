#!/usr/bin/env python3
"""Check that commit subjects follow the Conventional Commits format.

Usage:
    python scripts/check_commits.py [REV_RANGE]

REV_RANGE defaults to ``origin/main..HEAD``. Merge commits are skipped.
Exit status is 1 if any subject is not conventional, 0 otherwise.
"""

import re
import subprocess
import sys

TYPES = "feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert"
PATTERN = re.compile(rf"^({TYPES})(\([a-z0-9._/-]+\))?!?: \S.*$")
MAX_SUBJECT_LENGTH = 72


def problem_with(subject: str):
    """Return a short explanation if ``subject`` is not acceptable, else None."""
    if subject.startswith('Revert "'):
        return None  # git's own revert message is fine
    if not PATTERN.match(subject):
        return "expected '<type>(<optional scope>): <description>'"
    if len(subject) > MAX_SUBJECT_LENGTH:
        return f"subject is {len(subject)} characters (limit {MAX_SUBJECT_LENGTH})"
    return None


def is_conventional(subject: str) -> bool:
    return problem_with(subject) is None


def commit_subjects(rev_range: str):
    out = subprocess.run(
        ["git", "log", "--no-merges", "--format=%h%x1f%s", rev_range],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    for line in out.splitlines():
        short_hash, _, subject = line.partition("\x1f")
        yield short_hash, subject


def main(argv) -> int:
    rev_range = argv[1] if len(argv) > 1 else "origin/main..HEAD"
    failures = []
    count = 0
    for short_hash, subject in commit_subjects(rev_range):
        count += 1
        reason = problem_with(subject)
        if reason:
            failures.append((short_hash, subject, reason))
    if failures:
        print(f"{len(failures)} of {count} commit(s) need a better message:\n")
        for short_hash, subject, reason in failures:
            print(f"  {short_hash}  {subject}\n           -> {reason}")
        print("\nExample: feat(fees): add a grace period before fees start")
        return 1
    print(f"OK: {count} commit(s) follow Conventional Commits.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
