"""
ARMS Engine: ARAS Composite Risk Assessor (L3)

The highest authority on gross portfolio exposure. Consumes the 
Macro Compass score and applies the canonical equity ceiling limits.

Reference: ARMS FSD v1.1, Section 2 & Daily Monitor Spec
"""
from dataclasses import dataclass

@dataclass
class ArasOutput:
    regime: str
    score: float
    equity_ceiling_pct: float

def calculate_aras_ceiling(regime_score: float) -> ArasOutput:
    """
    Determines the absolute maximum gross equity exposure allowed based
    on the current regime score.
    """
    if regime_score <= 0.30:
        regime = "RISK_ON"
        ceiling = 1.00 # 100%
    elif regime_score <= 0.50:
        regime = "WATCH"
        ceiling = 1.00 # 100%
    elif regime_score <= 0.65:
        regime = "NEUTRAL"
        ceiling = 0.75 # 75%
    elif regime_score <= 0.80:
        regime = "DEFENSIVE"
        ceiling = 0.40 # 40%
    else:
        regime = "CRASH"
        ceiling = 0.15 # 15%

    return ArasOutput(regime=regime, score=regime_score, equity_ceiling_pct=ceiling)
