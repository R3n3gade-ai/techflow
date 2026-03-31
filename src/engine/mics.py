# src/engine/mics.py
# Implements the Model-Implied Conviction Score (MICS) formula.
# This is the data-driven brain for position sizing.

import json
import os
from dataclasses import dataclass
from typing import Literal, Dict

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

# --- Helper Functions ---

def _load_calibration_weights() -> Dict[str, float]:
    """
    Loads adjusted weights from the CCM module.
    Returns baseline weights if no calibration exists.
    """
    baseline = {
        "gate3_weight": 0.40,
        "gate6_weight": 0.30,
        "gate4_weight": 0.15,
        "gate5_weight": 0.15,
        "pm_alpha": 1.00
    }
    
    path = "achelion_arms/src/config/calibration_state.json"
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                cal = json.load(f)
                # Apply adjustments to baseline
                baseline["gate3_weight"] += cal.get("gate3_weight_adj", 0)
                baseline["gate6_weight"] += cal.get("gate6_weight_adj", 0)
                baseline["gate4_weight"] += cal.get("gate4_weight_adj", 0)
                baseline["gate5_weight"] += cal.get("gate5_weight_adj", 0)
                baseline["pm_alpha"] = cal.get("pm_performance_alpha", 1.0)
        except Exception:
            pass # Fallback to baseline
            
    return baseline

# --- Core Calculation Function ---

def calculate_mics(inputs: SentinelGateInputs) -> MICSResult:
    """
    Calculates the Model-Implied Conviction Score based on SENTINEL gate data.
    
    This function is the implementation of the formula from ARMS FSD v1.1, Section 11.1,
    augmented with the Phase 2 Conviction Calibration Module (CCM) loop.
    """

    # 0. Load (possibly calibrated) weights
    weights = _load_calibration_weights()

    # 1. Normalize Gate 3 score (0-30 -> 0-10)
    g3_score = (inputs.gate3_raw_score / 30) * 10

    # 2. Map Gate 6 source category to score
    source_scores = {'Cat A': 10, 'Cat B': 8, 'Cat C': 5, 'None': 4}
    g6_score = source_scores.get(inputs.source_category, 0)
    
    # Apply PM Alpha adjustment from CCM
    if inputs.source_category in ['Cat A', 'Cat B']:
        g6_score *= weights["pm_alpha"]

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
        (g3_score * weights["gate3_weight"]) +
        (g6_score * weights["gate6_weight"]) +
        (g4_score * weights["gate4_weight"]) +
        (g5_score * weights["gate5_weight"])
    )

    # 6. Round to nearest integer for the final C-level (1-10)
    conviction_level = max(1, min(10, round(mics_raw)))

    return MICSResult(raw_score=mics_raw, conviction_level=conviction_level)

