"""
ARMS Engine: CDF Analytics

Computes underperformance vs QQQ using live historical prices when available.
This reduces dependence on manual bridge-fed CDF state.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RelativePerformanceSnapshot:
    ticker: str
    qqq_return_45d: float
    position_return_45d: float
    underperformance_pp: float


def compute_underperformance_pp(position_price_45d_ago: Optional[float], position_price_now: Optional[float], qqq_price_45d_ago: Optional[float], qqq_price_now: Optional[float]) -> float:
    if not all(v is not None and v > 0 for v in [position_price_45d_ago, position_price_now, qqq_price_45d_ago, qqq_price_now]):
        return 0.0

    position_return = (position_price_now / position_price_45d_ago) - 1.0
    qqq_return = (qqq_price_now / qqq_price_45d_ago) - 1.0
    return max(0.0, (qqq_return - position_return) * 100.0)
