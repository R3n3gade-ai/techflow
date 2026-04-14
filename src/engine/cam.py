"""
ARMS Module: Coverage Adequacy Model (CAM)

This module extends the PTRH (Permanent Tail Risk Hedge) system by autonomously
calculating the required tail hedge coverage. It eliminates the need for any PM
discretion in sizing the tail hedge, making the process fully Tier 0.

The model uses four multipliers—regime, equity exposure, concentration, and
acute stress—to determine the adequate notional coverage in real-time.

Reference: ARMS Addendum 4 — Governing Principle + PTRH Coverage Adequacy Model
"""

from dataclasses import dataclass

# --- Placeholder for inputs from other ARMS modules ---
# In a live system, these values would be fetched from their respective modules.

@dataclass
class CamInputs:
    """
    Represents all the live data points required for the CAM calculation.
    """
    current_equity_pct: float
    regime_score: float
    fem_concentration_score: float
    macro_stress_score: float
    cdm_active_signals: int
    nav: float

# --- CAM Formula Constants (as per Addendum 4, Section 3.2) ---

BASE_COVERAGE_PCT = 0.012

# --- CAM Core Logic ---

def get_regime_table_minimum(regime_score: float) -> float:
    """
    Returns the minimum required coverage percentage based on the regime table.
    This acts as a floor for the CAM calculation.
    
    PTRH regime multiplier table (CLAUDE.md v4.0):
      RISK_ON  (<0.30): 1.0× base = 1.2% NAV
      WATCH    (0.30-0.50): 1.25× base = 1.5% NAV
      NEUTRAL  (0.51-0.65): 1.25× base = 1.5% NAV
      DEFENSIVE(0.66-0.80): 1.5× base = 1.8% NAV
      CRASH    (>0.80): 2.0× base = 2.4% NAV
    """
    if regime_score < 0.30:  # RISK_ON
        return 0.012  # 1.2%
    elif regime_score <= 0.50:  # WATCH
        return 0.015  # 1.5%
    elif regime_score <= 0.65:  # NEUTRAL
        return 0.015  # 1.5%
    elif regime_score <= 0.80:  # DEFENSIVE
        return 0.018  # 1.8%
    else:  # CRASH
        return 0.024  # 2.4%

def calculate_required_notional(inputs: CamInputs) -> float:
    """
    Calculates the required QQQ put notional in dollars based on current risk factors.

    Args:
        inputs: A dataclass containing all necessary live data points.

    Returns:
        The required notional value of the tail hedge in dollars.
    """
    # Multiplier 1: Regime Score
    regime_multiplier = 1.0 + inputs.regime_score

    # Multiplier 2: Equity Exposure
    equity_multiplier = 0.67 + (inputs.current_equity_pct * 0.33)

    # Multiplier 3: FEM Concentration
    if inputs.fem_concentration_score > 0.80:
        concentration_multiplier = 1.30
    elif inputs.fem_concentration_score > 0.65:
        concentration_multiplier = 1.15
    else:
        concentration_multiplier = 1.00

    # Multiplier 4: Acute Stress (Macro + CDM)
    stress_multiplier = 1.0 + (inputs.macro_stress_score * 0.40)
    stress_multiplier += (inputs.cdm_active_signals * 0.03)
    stress_multiplier = min(stress_multiplier, 1.60)  # Cap at 1.60x

    # Calculate the raw required coverage percentage
    required_pct = (
        BASE_COVERAGE_PCT *
        regime_multiplier *
        equity_multiplier *
        concentration_multiplier *
        stress_multiplier
    )

    # Apply floor based on the static regime table
    regime_minimum_pct = get_regime_table_minimum(inputs.regime_score)
    required_pct = max(required_pct, regime_minimum_pct)

    # Apply ceiling to prevent over-hedging
    required_pct = min(required_pct, 0.035)  # Max 3.5% of NAV

    return required_pct * inputs.nav

if __name__ == '__main__':
    # --- Test Case from Addendum 4, Section 3.3 ---
    print("Running CAM calculation for worked example (March 27, 2026 conditions)...")

    # Inputs representing the high-stress scenario from the document
    current_conditions = CamInputs(
        current_equity_pct=0.40,      # 40% (DEFENSIVE ceiling)
        regime_score=0.79,
        fem_concentration_score=0.82, # ALERT
        macro_stress_score=0.85,
        cdm_active_signals=2,
        nav=50_000_000               # Example $50M NAV
    )

    required_notional = calculate_required_notional(current_conditions)
    required_percentage = (required_notional / current_conditions.nav) * 100

    print(f"Inputs: {current_conditions}")
    print(f"Required Notional: ${required_notional:,.2f}")
    print(f"Required Coverage: {required_percentage:.2f}% of NAV")
    
    # Verification based on the document's worked example
    # Expected result is ~3.12% of NAV
    assert 3.10 < required_percentage < 3.15, "Calculation does not match worked example."
    print("\nWorked example test passed.")

    # --- Test Case for RISK_ON baseline ---
    print("\nRunning CAM calculation for baseline RISK_ON conditions...")
    
    baseline_conditions = CamInputs(
        current_equity_pct=1.0,       # 100%
        regime_score=0.25,
        fem_concentration_score=0.40, # NORMAL
        macro_stress_score=0.20,
        cdm_active_signals=0,
        nav=50_000_000
    )

    required_notional_base = calculate_required_notional(baseline_conditions)
    required_percentage_base = (required_notional_base / baseline_conditions.nav) * 100

    print(f"Inputs: {baseline_conditions}")
    print(f"Required Notional: ${required_notional_base:,.2f}")
    print(f"Required Coverage: {required_percentage_base:.2f}% of NAV")

    # Verification: should be close to the regime minimum of 1.2%
    assert 1.20 <= required_percentage_base < 1.25, "Baseline calculation is incorrect."
    print("\nBaseline test passed.")
