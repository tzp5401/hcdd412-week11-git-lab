# HCDD 412, Week 11: Git Workflow Lab (Starter Repo)

Practice repo for the Week 11 individual assignment, **Git Workflow Lab: Branching, PR, Conflict Resolution**. You will create a feature branch, review a simulated teammate's pull request, open your own pull request that conflicts with it, resolve the conflict (with AI help, and with your judgment in charge), and merge.

The full walkthrough is in the **Week 11 Lab Guide** posted in Canvas. This README covers setup only.

## What is in here

| Path | Purpose |
| --- | --- |
| `src/campusfees/fees.py` | The code you will change: `late_fee()` for a campus library desk |
| `tests/` | Tests for `late_fee()` plus tests for the lab's own check scripts |
| `docs/fee-policy.md` | The written fee policy you will update alongside the code |
| `.github/workflows/ci.yml` | CI: lint, tests, conflict-marker scan, and a Conventional Commits check on pull requests |
| `.github/pull_request_template.md` | The PR template GitHub pre-fills for you. Use it honestly |
| `.github/CODEOWNERS` | Inert in this lab (commented out). Your team project will use it |
| `lab/simulate_teammate.py` | Creates "Taylor Teammate's" conflicting branch (Lab Guide, Part 3) |
| `lab/verify_lab.py` | Self-check to run before you write your reflection |
| `scripts/` | The commit-message and conflict-marker checkers that CI runs |

## Setup

You need **Git**, **Python 3.10 or newer**, and **VS Code** with the GitHub Copilot extension (from Week 1).

1. On GitHub, click **Use this template**, then **Create a new repository**. Name it `hcdd412-week11-git-lab` and keep it **Public** (branch rules are free on public repositories, and your instructor needs to see it).
2. Clone your new repository and open it in VS Code.
3. Create a virtual environment and install dependencies.

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell refuses to run the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again.

4. Confirm everything is green before you change anything:

```bash
flake8 src tests scripts lab
pytest -q
```

5. Make sure your default branch is named `main`:

```bash
git branch --show-current
```

## Check your work

After the final merge, switch to `main`, pull, and run:

```bash
python lab/verify_lab.py
```

It checks the combined behavior, your docs and tests, your commit messages, and that your history shows real merges. It is a self-check, not your grade.

## Ground rules

- Use **Conventional Commits** for every commit you write: `feat(fees): add a grace period before fees start`.
- Merge both pull requests with **Create a merge commit** (not squash, not rebase) so the conflict resolution stays visible in history.
- Disclose all AI assistance in your pull request and in your reflection, per the course AI Tool Usage Policy. You must be able to explain every line you submit.
