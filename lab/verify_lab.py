#!/usr/bin/env python3
"""Self-check for the Week 11 Git Workflow Lab.

Run it from the repo root, on ``main``, after the final merge and a
``git pull``:

    python lab/verify_lab.py

This is a self-check, not your grade. It confirms the final code and history
look right before you write your reflection and submit.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from check_commits import is_conventional  # noqa: E402
from check_conflict_markers import find_markers, tracked_files  # noqa: E402

TEAMMATE = "Taylor Teammate"


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout


def check_no_markers():
    hits = []
    for name in tracked_files():
        try:
            text = (ROOT / name).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        hits += [f"{name}:{n}" for n, _ in find_markers(text)]
    if hits:
        return False, "markers in " + ", ".join(hits)
    return True, "no conflict markers"


def check_behavior():
    try:
        from campusfees import late_fee

        cases = [
            (dict(days_late=10, daily_rate=0.5, grace_days=3), 3.5),
            (dict(days_late=10, daily_rate=0.5, max_fee=2.0), 2.0),
            (dict(days_late=10, daily_rate=0.5, grace_days=3, max_fee=2.0), 2.0),
            (dict(days_late=4, daily_rate=1.0, grace_days=1, max_fee=10.0), 3.0),
            (dict(days_late=2, daily_rate=1.0, grace_days=2), 0.0),
            (dict(days_late=0, daily_rate=1.0, grace_days=0, max_fee=5.0), 0.0),
        ]
        for kwargs, expected in cases:
            actual = late_fee(**kwargs)
            if actual != expected:
                return False, f"late_fee({kwargs}) returned {actual}, expected {expected}"
    except TypeError as error:
        return False, f"late_fee() is missing a parameter: {error}"
    except Exception as error:  # noqa: BLE001 - report any import/runtime problem
        return False, f"could not run late_fee(): {error}"
    return True, "late_fee() supports grace_days and max_fee together"


def check_policy_doc():
    text = (ROOT / "docs" / "fee-policy.md").read_text(encoding="utf-8").lower()
    if "grace" in text and "maximum" in text:
        return True, "policy doc records both rules"
    return False, "docs/fee-policy.md must mention both the grace period and the maximum fee"


def check_tests_cover_both():
    text = (ROOT / "tests" / "test_fees.py").read_text(encoding="utf-8")
    if "grace" in text and "max_fee" in text:
        return True, "tests cover both features"
    return False, "tests/test_fees.py should test both grace_days and max_fee"


def check_teammate_commit_present():
    log = git("log", "--format=%an", "HEAD")
    if TEAMMATE in log.splitlines():
        return True, "teammate's commit is in history"
    return False, "Taylor's commit is not in history; merge the feature/fee-cap PR first"


def check_merge_commits():
    count = int(git("rev-list", "--merges", "--count", "HEAD").strip())
    if count >= 2:
        return True, f"{count} merge commit(s) in history"
    return False, (
        f"found {count} merge commit(s); expected at least 2 "
        "(use 'Create a merge commit' for both PRs)"
    )


def check_commit_messages():
    bad = []
    for line in git("log", "--no-merges", "--format=%H%x1f%an%x1f%P%x1f%s", "HEAD").splitlines():
        _hash, author, parents, subject = line.split("\x1f", 3)
        if author == TEAMMATE or not parents.strip():
            continue  # teammate's commit and the template's root commit are exempt
        if not is_conventional(subject):
            bad.append(subject)
    if bad:
        return False, "fix these messages: " + "; ".join(bad)
    return True, "your commit messages follow Conventional Commits"


def check_branch():
    branch = git("branch", "--show-current").strip()
    if branch == "main":
        return True, "on main"
    return False, f"you are on '{branch}'; switch to main and pull first"


CHECKS = [
    ("On main", check_branch),
    ("No conflict markers", check_no_markers),
    ("Combined behavior", check_behavior),
    ("Policy doc updated", check_policy_doc),
    ("Tests added", check_tests_cover_both),
    ("Teammate PR merged", check_teammate_commit_present),
    ("Merge commits", check_merge_commits),
    ("Commit messages", check_commit_messages),
]


def main() -> int:
    failed = 0
    print("Week 11 lab self-check\n")
    for label, check in CHECKS:
        ok, detail = check()
        failed += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {detail}")
    print()
    if failed:
        print(f"{failed} check(s) need attention.")
        return 1
    print("All checks passed. Now write your 300-word reflection and submit your repo link.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
