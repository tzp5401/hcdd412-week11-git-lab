import pytest

from check_commits import is_conventional, problem_with


@pytest.mark.parametrize(
    "subject",
    [
        "feat(fees): add a grace period before fees start",
        "fix: stop negative days from producing a fee",
        "docs(policy): describe the maximum fee",
        "test(fees): cover cap and grace period together",
        "refactor(fees)!: rename late_fee parameters",
        'Revert "feat(fees): add a grace period"',
    ],
)
def test_accepts_conventional_subjects(subject):
    assert is_conventional(subject)


@pytest.mark.parametrize(
    "subject",
    [
        "update stuff",
        "Fixed the bug",
        "feat add grace period",
        "feat:no space after colon",
        "FEAT(fees): shouty type",
        "wip",
    ],
)
def test_rejects_vague_or_malformed_subjects(subject):
    assert not is_conventional(subject)


def test_rejects_overlong_subject():
    subject = "feat(fees): " + "x" * 80
    assert "characters" in problem_with(subject)
