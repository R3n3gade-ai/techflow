"""
ARMS Engine: Regime Probability Engine (RPE)

This module provides an anticipatory layer to the ARMS system. Instead of
just reacting to the current regime, the RPE calculates the probability
distribution of the next regime transition based on the velocity and
volatility of key macro signals.

Reference: arms_fsd_master_build_v1.1.md, Section 5.1
"""

from dataclasses import dataclass, field
from typing import List, Dict, Literal
from collections import deque

# --- Data Structures ---

@dataclass
class RegimeProbabilitySignal:
    """The output of the RPE, providing a forward-looking view."""
    current_regime: str
    transition_probabilities: Dict[str, float] = field(default_factory=dict)
    highest_prob_transition: str = "STABLE"
    highest_prob_value: float = 1.0
    
# A simple in-memory store for recent signal values to calculate momentum.
# In a real system, this would be backed by a time-series database.
SIGNAL_HISTORY: Dict[str, deque] = {
    "T10Y2Y": deque(maxlen=5),
    "HY_CREDIT_SPREAD": deque(maxlen=5)
}

# --- RPE Logic ---

def calculate_rpe(
    current_regime: str,
    current_regime_score: float,
    latest_signals: List # Expects List[SignalRecord]
) -> RegimeProbabilitySignal:
    """
    Calculates the regime transition probabilities.
    
    This is a simplified model based on signal momentum (rate of change).
    A positive momentum in a risk-off signal (like credit spreads) increases
    the probability of moving to a more defensive regime.
    """
    
    # 1. Update signal history
    for signal in latest_signals:
        if signal.signal_type in SIGNAL_HISTORY:
            SIGNAL_HISTORY[signal.signal_type].append(signal.raw_value)

    # 2. Calculate momentum for key signals
    # Momentum = (current_value - oldest_value)
    spread_momentum = 0.0
    if len(SIGNAL_HISTORY["HY_CREDIT_SPREAD"]) == 5:
        spread_history = SIGNAL_HISTORY["HY_CREDIT_SPREAD"]
        spread_momentum = spread_history[-1] - spread_history[0] # Positive is bad (widening)

    yield_curve_momentum = 0.0
    if len(SIGNAL_HISTORY["T10Y2Y"]) == 5:
        yield_history = SIGNAL_HISTORY["T10Y2Y"]
        yield_curve_momentum = yield_history[-1] - yield_history[0] # Negative is bad (inverting)

    # 3. Generate a score based on momentum
    # This is a highly simplified heuristic model.
    # A positive score suggests a move to a more defensive regime.
    risk_off_momentum = (spread_momentum * 10) - (yield_curve_momentum * 5)
    
    # 4. Define transition probabilities
    probs = {"STABLE": 1.0, "RISK_ON": 0.0, "WATCH": 0.0, "NEUTRAL": 0.0, "DEFENSIVE": 0.0, "CRASH": 0.0}
    
    next_defensive_regime = ""
    next_offensive_regime = ""
    if current_regime == "DEFENSIVE":
        next_defensive_regime = "CRASH"
        next_offensive_regime = "NEUTRAL"
    elif current_regime == "NEUTRAL":
        next_defensive_regime = "DEFENSIVE"
        next_offensive_regime = "WATCH"
    # ... and so on for all regimes

    if risk_off_momentum > 0.3 and next_defensive_regime: # Strong risk-off momentum
        prob_defensive = min(0.6, risk_off_momentum) # Cap probability
        probs[next_defensive_regime] = prob_defensive
        probs["STABLE"] -= prob_defensive
    elif risk_off_momentum < -0.3 and next_offensive_regime: # Strong risk-on momentum
        prob_offensive = min(0.6, abs(risk_off_momentum))
        probs[next_offensive_regime] = prob_offensive
        probs["STABLE"] -= prob_offensive
        
    # Find the highest probability transition
    highest_prob_item = max(probs.items(), key=lambda item: item[1])

    return RegimeProbabilitySignal(
        current_regime=current_regime,
        transition_probabilities=probs,
        highest_prob_transition=highest_prob_item[0],
        highest_prob_value=highest_prob_item[1]
    )

if __name__ == '__main__':
    from data_feeds.feed_interface import SignalRecord
    
    print("--- Running RPE Test Case (Worsening Conditions) ---")
    
    # Simulate a history of worsening credit spreads
    SIGNAL_HISTORY["HY_CREDIT_SPREAD"].extend([3.5, 3.6, 3.7, 3.8, 3.9])
    # Simulate a flattening yield curve
    SIGNAL_HISTORY["T10Y2Y"].extend([0.25, 0.22, 0.20, 0.18, 0.15])
    
    latest_mock_signals = [
        SignalRecord('MACRO', 'HY_CREDIT_SPREAD', 0.8, 3.9, 'MOCK', '', 'FREE'),
        SignalRecord('MACRO', 'T10Y2Y', 0.3, 0.15, 'MOCK', '', 'FREE'),
    ]
    
    rpe_signal = calculate_rpe("NEUTRAL", 0.60, latest_mock_signals)
    
    print(rpe_signal)
    
    # Expected: Spread momentum is 3.9-3.5 = 0.4. Curve momentum is 0.15-0.25 = -0.10
    # Risk-off score = (0.4 * 10) - (-0.10 * 5) = 4 + 0.5 = 4.5. Very high.
    # Probability of moving to DEFENSIVE should be high.
    self.assertEqual(rpe_signal.highest_prob_transition, "DEFENSIVE")
    self.assertGreater(rpe_signal.transition_probabilities["DEFENSIVE"], 0.5)
    
    print("\nWorsening conditions test PASSED.")
    
    print("\n--- Running RPE Test Case (Improving Conditions) ---")
    
    # Simulate a history of improving credit spreads
    SIGNAL_HISTORY["HY_CREDIT_SPREAD"].extend([3.9, 3.8, 3.7, 3.6, 3.5])
    # Simulate a steepening yield curve
    SIGNAL_HISTORY["T10Y2Y"].extend([0.15, 0.18, 0.20, 0.22, 0.25])
    
    latest_mock_signals_2 = [
        SignalRecord('MACRO', 'HY_CREDIT_SPREAD', 0.6, 3.5, 'MOCK', '', 'FREE'),
        SignalRecord('MACRO', 'T10Y2Y', 0.5, 0.25, 'MOCK', '', 'FREE'),
    ]
    
    rpe_signal_2 = calculate_rpe("NEUTRAL", 0.60, latest_mock_signals_2)
    
    print(rpe_signal_2)
    
    # Expected: Spread momentum is -0.4. Curve momentum is 0.10.
    # Risk-off score = (-0.4 * 10) - (0.10 * 5) = -4 - 0.5 = -4.5.
    # Probability of moving to WATCH should be high.
    self.assertEqual(rpe_signal_2.highest_prob_transition, "WATCH")
    self.assertGreater(rpe_signal_2.transition_probabilities["WATCH"], 0.5)
    print("\nImproving conditions test PASSED.")
    
