from check_conflict_markers import find_markers


def test_detects_all_three_marker_lines():
    text = "\n".join(
        ["a = 1", "<" * 7 + " HEAD", "b = 2", "=" * 7, "b = 3", ">" * 7 + " feature/x", "c = 4"]
    )
    assert [number for number, _ in find_markers(text)] == [2, 4, 6]


def test_ignores_ordinary_text():
    text = "Title\n=====\n\nUse == for comparison, and <<< sparingly.\n"
    assert find_markers(text) == []
