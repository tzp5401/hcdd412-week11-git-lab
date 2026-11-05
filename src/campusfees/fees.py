"""Late-fee calculation for the campus library desk."""


def late_fee(days_late: int, daily_rate: float, grace_days: int = 0) -> float:
    """Return the late fee after ``grace_days`` free days.

    Items returned on time or early, or within the grace period, are never
    charged.
    """
    chargeable_days = days_late - grace_days
    if chargeable_days <= 0:
        return 0.0
    return round(chargeable_days * daily_rate, 2)
