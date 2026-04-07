"""
ARMS Engine: Factor Exposure Monitor (FEM)

Advisory sub-module that detects hidden concentration risk.
Flags the PM when correlated exposure becomes too high.

Reference: THB v4.0, Section 2
"""
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class FactorExposureSignal:
    factors: Dict[str, float]
    status: str
    highest_exposure_factor: str
    highest_exposure_pct: float

def run_fem_check(portfolio_weights: Dict[str, float]) -> FactorExposureSignal:
    # Simplified mapping for Phase 1
    ai_capex_names = ['NVDA', 'AMD', 'ALAB', 'MU', 'MRVL', 'AVGO', 'ANET', 'ARM']
    
    ai_exposure = sum(weight for ticker, weight in portfolio_weights.items() if ticker in ai_capex_names)
    
    status = "NORMAL"
    if ai_exposure > 0.80:
        status = "ALERT"
    elif ai_exposure > 0.65:
        status = "WATCH"
        
    return FactorExposureSignal(
        factors={"AI_CAPEX_CYCLE": ai_exposure},
        status=status,
        highest_exposure_factor="AI_CAPEX_CYCLE",
        highest_exposure_pct=ai_exposure
    )
