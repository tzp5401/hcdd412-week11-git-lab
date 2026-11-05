"""Late-fee calculation for the campus library desk."""

from typing import Optional


def late_fee(
    days_late: int,
    daily_rate: float,
    grace_days: int = 0,
    max_fee: Optional[float] = None,
) -> float:
    """Return the late fee after applying the grace period and maximum fee limits.

    Items returned on time or early are never charged.
    The first grace_days days late are free.
    Only the days after the grace period are charged.
    When ``max_fee`` is given, the fee never exceeds it.
    """
    if days_late <= 0:
        return 0.0

    chargeable_days = max(0, days_late - grace_days)
    fee = round(chargeable_days * daily_rate, 2)

    if max_fee is not None:
        fee = min(fee, max_fee)

    return fee
