"""
ARMS Engine: Crypto Microstructure

ARAS Sub-Module evaluating crypto market health via CME futures basis
(funding rate proxy) and open interest stress from the IBKR crypto feed.

The BTC_FUNDING value is normalized [0, 1] where:
  0.0 = deep backwardation (bearish stress)
  0.5 = flat basis (neutral)
  1.0 = strong contango (bullish)

The BTC_OI value is normalized [0, 1] where higher = more stress
(rising volume + falling price).

Reference: THB v4.0, Section 10
"""
from dataclasses import dataclass
from typing import List
from data_feeds.interfaces import SignalRecord

@dataclass
class CryptoMicrostructureSignal:
    status: str
    stress_score: float

def run_crypto_microstructure_check(signals: List[SignalRecord]) -> CryptoMicrostructureSignal:
    # BTC funding basis proxy (0-1 normalized, 0.5 = neutral)
    funding = next((s.value for s in signals if s.signal_type == 'BTC_FUNDING'), 0.5)
    # OI/volume stress proxy (0-1, higher = more stress)
    oi_stress = next((s.value for s in signals if s.signal_type == 'BTC_OI'), 0.0)

    # Backwardation (funding < 0.3) or high OI stress (> 0.6) = bearish
    if funding < 0.20 or oi_stress > 0.70:
        status = "CRITICAL"
        stress = 0.9
    elif funding < 0.35 or oi_stress > 0.40:
        status = "ELEVATED"
        stress = 0.6
    else:
        status = "NORMAL"
        stress = 0.1

    return CryptoMicrostructureSignal(status=status, stress_score=stress)
