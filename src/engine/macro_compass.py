"""
ARMS Engine: Macro Compass (L2)

This module calculates the core Macro Regime Score (0.0 to 1.0)
from incoming data pipeline signals.

Reference: ARMS FSD v1.1, Section 1 & 2
"""
from typing import List, Dict
from data_feeds.interfaces import SignalRecord

def calculate_macro_regime_score(signals: List[SignalRecord]) -> float:
    """
    Computes a simplified, robust baseline macro regime score from raw inputs.
    In a full production implementation, this is a complex non-linear weighted 
    model based on VIX, Credit Spreads, Yield Curve, and PMI.
    
    Returns a score between 0.0 (Perfect Risk On) and 1.0 (Absolute Crash).
    """
    if not signals:
        return 0.50 # Default to NEUTRAL if blinded

    # Extract signals or use safe defaults
    vix = next((s.value for s in signals if s.signal_type == 'VIX_INDEX'), 20.0)
    hy_spread = next((s.value for s in signals if s.signal_type == 'HY_CREDIT_SPREAD'), 4.0)
    pmi = next((s.value for s in signals if s.signal_type == 'PMI_NOWCAST'), 50.0)

    # Base normalization (0.0 to 1.0 stress scales)
    # VIX: 10 (0.0) to 45 (1.0)
    v_stress = max(0.0, min(1.0, (vix - 10) / 35.0))
    
    # HY Spread: 3.0 (0.0) to 8.0 (1.0)
    h_stress = max(0.0, min(1.0, (hy_spread - 3.0) / 5.0))
    
    # PMI: 55 (0.0) to 45 (1.0) -> Inverse
    p_stress = max(0.0, min(1.0, (55.0 - pmi) / 10.0))

    # Weighting: VIX 40%, Spread 40%, PMI 20%
    composite_score = (v_stress * 0.40) + (h_stress * 0.40) + (p_stress * 0.20)
    
    # Bound safely
    return max(0.0, min(1.0, composite_score))

def get_regime_label(score: float) -> str:
    """
    Maps a 0.0-1.0 score to the canonical 5-tier ARAS regime label.
    Reference: Daily Monitor Spec
    """
    if score <= 0.30: return "RISK_ON"
    if score <= 0.50: return "WATCH"
    if score <= 0.65: return "NEUTRAL"
    if score <= 0.80: return "DEFENSIVE"
    return "CRASH"
