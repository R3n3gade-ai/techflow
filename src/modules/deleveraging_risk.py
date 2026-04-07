"""
ARMS Engine: Deleveraging Risk

ARAS Sub-Module tracking the velocity of deleveraging in the market.
Uses high-yield spreads and implied volatility (VIX) to flag systemic 
deleveraging cycles.

Reference: THB v4.0, Section 10
"""
from dataclasses import dataclass
from typing import List
from data_feeds.interfaces import SignalRecord

@dataclass
class DeleveragingSignal:
    status: str
    velocity_score: float

def run_deleveraging_check(signals: List[SignalRecord]) -> DeleveragingSignal:
    vix = next((s.value for s in signals if s.signal_type == 'VIX_INDEX'), 20.0)
    hy_spread = next((s.value for s in signals if s.signal_type == 'HY_CREDIT_SPREAD'), 4.0)

    # Simple velocity model: if HY spread > 5.5% and VIX > 30, deleveraging is active
    if hy_spread > 5.5 and vix > 30.0:
        status = "ACTIVE"
        velocity = 0.8
    elif hy_spread > 4.5 and vix > 20.0:
        status = "WATCH"
        velocity = 0.5
    else:
        status = "NORMAL"
        velocity = 0.1

    return DeleveragingSignal(status=status, velocity_score=velocity)
