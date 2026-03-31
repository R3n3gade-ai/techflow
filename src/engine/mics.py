# src/engine/mics.py
# Implements the Model-Implied Conviction Score (MICS) formula.
# This is the data-driven brain for position sizing.

from dataclasses import dataclass
from typing import Literal

# --- Data Structures for Inputs ---

@dataclass
class SentinelGateInputs:
    """
    All the data required from the SENTINEL v2.0 protocol to calculate MICS.
    """
    gate3_raw_score: float  # The quantitative mispricing score (0-30).
    source_category: Literal['Cat A', 'Cat B', 'Cat C', 'None'] # PM's source declaration.
    fem_impact: str         # Factor Exposure Monitor impact, e.g., 'NORMAL->WATCH'.
    regime_at_entry: str    # Market regime at time of entry, e.g., 'RISK_ON'.


@dataclass
class MICSResult:
    """
    The output of the MICS calculation.
    """
    raw_score: float        # The precise MICS score, float from 0.0-10.0.
    conviction_level: int   # The final C-level, integer from 1-10.

# --- Core Calculation Function ---

def calculate_mics(inputs: SentinelGateInputs) -> MICSResult:
    """
    Calculates the Model-Implied Conviction Score based on SENTINEL gate data.
    
    This function is the implementation of the formula from ARMS FSD v1.1, Section 11.1.
    """

    # Component weights — sum to 1.0
    gate3_weight = 0.40  # Quantitative mispricing — core signal
    gate6_weight = 0.30  # Source quality — information edge
    gate4_weight = 0.15  # FEM impact — portfolio cleanliness
    gate5_weight = 0.15  # Regime timing — entry quality

    # 1. Normalize Gate 3 score (0-30 -> 0-10)
    g3_score = (inputs.gate3_raw_score / 30) * 10

    # 2. Map Gate 6 source category to score
    source_scores = {'Cat A': 10, 'Cat B': 8, 'Cat C': 5, 'None': 4}
    g6_score = source_scores.get(inputs.source_category, 0) # Default to 0 if invalid category

    # 3. Map Gate 4 FEM impact to score
    fem_scores = {
        'NORMAL->NORMAL': 10,
        'NORMAL->WATCH': 7,
        'WATCH->WATCH': 6,
        'WATCH->ALERT (paired trim)': 4
    }
    g4_score = fem_scores.get(inputs.fem_impact, 0)

    # 4. Map Gate 5 regime timing to score
    regime_scores = {
        'RISK_ON': 10,
        'WATCH': 9,
        'NEUTRAL': 7,
        'NEUTRAL (queued)': 5
    }
    g5_score = regime_scores.get(inputs.regime_at_entry, 0)

    # 5. Calculate weighted average for raw score
    mics_raw = (
        (g3_score * gate3_weight) +
        (g6_score * gate6_weight) +
        (g4_score * gate4_weight) +
        (g5_score * gate5_weight)
    )

    # 6. Round to nearest integer for the final C-level (1-10)
    conviction_level = max(1, min(10, round(mics_raw)))

    return MICSResult(raw_score=mics_raw, conviction_level=conviction_level)

