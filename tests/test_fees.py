from campusfees import late_fee


def test_on_time_return_is_free():
    assert late_fee(0, 0.25) == 0.0


def test_early_return_is_free():
    assert late_fee(-2, 0.25) == 0.0


def test_one_day_late():
    assert late_fee(1, 0.25) == 0.25


def test_multiple_days_late():
    assert late_fee(4, 0.25) == 1.0


def test_fee_rounds_to_cents():
    assert late_fee(3, 0.333) == 1.0
