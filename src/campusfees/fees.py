"""Late-fee calculation for the campus library desk."""


def late_fee(days_late: int, daily_rate: float) -> float:
    """Return the late fee in dollars for an item returned ``days_late`` days late.

    Items returned on time or early are never charged.
    """
    if days_late <= 0:
        return 0.0
    return round(days_late * daily_rate, 2)
