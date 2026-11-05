"""Late-fee calculation for the campus library desk."""

from typing import Optional


def late_fee(days_late: int, daily_rate: float, max_fee: Optional[float] = None) -> float:
    """Return the late fee in dollars for an item returned ``days_late`` days late.

    Items returned on time or early are never charged. When ``max_fee`` is
    given, the fee never exceeds it.
    """
    if days_late <= 0:
        return 0.0
    fee = round(days_late * daily_rate, 2)
    if max_fee is not None:
        fee = min(fee, max_fee)
    return fee
