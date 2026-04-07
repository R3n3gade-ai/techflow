"""
ARMS Engine: Crypto Microstructure

ARAS Sub-Module evaluating crypto market health (Funding rates, 
liquidations, open interest) as a leading liquidity indicator.

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
    funding = next((s.value for s in signals if s.signal_type == 'BTC_FUNDING'), 0.01)
    liq_vol = next((s.value for s in signals if s.signal_type == 'LIQ_VOL_24H'), 1.0)

    if funding < -0.05 or liq_vol > 3.0:
        status = "CRITICAL"
        stress = 0.9
    elif funding < 0.0 or liq_vol > 2.0:
        status = "ELEVATED"
        stress = 0.6
    else:
        status = "NORMAL"
        stress = 0.1

    return CryptoMicrostructureSignal(status=status, stress_score=stress)
