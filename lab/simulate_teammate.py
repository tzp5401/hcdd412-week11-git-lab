#!/usr/bin/env python3
"""Create the simulated teammate's branch for the Week 11 Git lab.

Run this AFTER you have committed your own ``feature/grace-period`` work and
BEFORE you merge anything into ``main``:

    python lab/simulate_teammate.py

It creates a local branch named ``feature/fee-cap`` from ``main`` with one
commit authored by "Taylor Teammate", then switches you back to the branch you
were on. Taylor's change touches the same lines you touched, which is what
produces the merge conflict you will resolve.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEAMMATE_DIR = ROOT / "lab" / "teammate"
BRANCH = "feature/fee-cap"
AUTHOR_NAME = "Taylor Teammate"
AUTHOR_EMAIL = "taylor.teammate@example.com"
MESSAGE = "feat(fees): cap late fee at a configurable maximum"
BASE_SIGNATURE = "def late_fee(days_late: int, daily_rate: float) -> float:"


def git(*args, check=True):
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, capture_output=True, text=True
    )


def fail(message):
    print(f"\nStopped: {message}")
    sys.exit(1)


def main() -> None:
    if git("rev-parse", "--is-inside-work-tree", check=False).returncode != 0:
        fail("this folder is not a Git repository. Run 'git init' or clone your repo first.")

    original = git("branch", "--show-current").stdout.strip()
    if not original:
        fail("you are in a detached-HEAD state. Switch to your feature branch first.")
    if original == "main":
        fail("you are on main. Create and commit your own feature branch first "
             "(see the Lab Guide, Part 2).")
    if git("status", "--porcelain").stdout.strip():
        fail("you have uncommitted changes. Commit or stash them, then run this again.")
    if git("rev-parse", "--verify", "--quiet", BRANCH, check=False).returncode == 0:
        fail(f"a branch named {BRANCH} already exists. Delete it with "
             f"'git branch -D {BRANCH}' to start over.")

    main_file = git("show", "main:src/campusfees/fees.py", check=False)
    if main_file.returncode != 0:
        fail("could not find a local 'main' branch. Run 'git branch -M main' if yours has "
             "another name.")
    if BASE_SIGNATURE not in main_file.stdout:
        fail("main has already changed late_fee(). Run this script before merging "
             "anything into main.")

    git("switch", "-c", BRANCH, "main")
    for source in sorted(TEAMMATE_DIR.rglob("*")):
        if source.is_file():
            target = ROOT / source.relative_to(TEAMMATE_DIR)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    git("add", "-A")
    git(
        "-c", f"user.name={AUTHOR_NAME}",
        "-c", f"user.email={AUTHOR_EMAIL}",
        "commit", "-m", MESSAGE,
    )
    git("switch", original)

    print(f"Created {BRANCH} with one commit by {AUTHOR_NAME}.")
    print(f"You are back on {original}.\n")
    print("Next (Lab Guide, Part 3):")
    print(f"  1. git push -u origin {BRANCH}")
    print("  2. Open a pull request for it on GitHub and review it like a teammate's PR.")
    print("  3. Merge it into main using 'Create a merge commit'.")
    print(f"  4. Then open the pull request for {original}: GitHub will report a conflict.")


if __name__ == "__main__":
    main()
