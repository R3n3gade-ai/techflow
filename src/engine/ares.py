"""
ARMS Engine: ARES (Re-Entry System) & VARES

This module provides the Tier 0 autonomous re-entry logic for ARMS. It 
prevents premature re-exposure after a crash by requiring three specific 
gates to clear before deploying capital in staged tranches (25/50/75/100%).

"Silence is trust in the architecture."

Reference: ARMS v4.0 Briefing, Section 1.2 & 4.1
Reference: Codebase Game Plan v2.0, Step 5
"""

import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Literal, Optional

# --- Internal Imports ---
from data_feeds.interfaces import SignalRecord
from execution.order_request import OrderRequest
from reporting.audit_log import SessionLogEntry, append_to_log

# --- Data Structures ---

@dataclass
class AresStatus:
    """Represents the current state of the Re-Entry System."""
    gates_cleared: List[str]
    is_fully_cleared: bool
    current_tranche_level: int # 1=25%, 2=50%, 3=75%, 4=100%
    vares_multiplier: float
    next_tranche_available_at: Optional[str]
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

# --- Configuration ---

REENTRY_TRANCHES = {
    1: 0.25,
    2: 0.50,
    3: 0.75,
    4: 1.00
}

# Days required between tranche deployments to ensure stability
TRANCHE_COOLDOWN_DAYS = 7

# --- ARES Logic ---

def run_ares_check(
    current_regime: str,
    regime_score: float,
    macro_stress_score: float, # 0.0 - 1.0 (VIX/Spreads)
    retail_sentiment_score: float, # 0.0 - 1.0 (Capitulation indicator)
    last_tranche_deployed_at: Optional[datetime.datetime] = None,
    current_tranche_level: int = 0
) -> AresStatus:
    """
    Evaluates the 3 re-entry gates and determines the VARES sizing.
    """
    gates_cleared = []
    
    # Gate 1: Stress Normalization
    # Requirement: Macro Stress Score < 0.40 (Calm returning)
    if macro_stress_score < 0.40:
        gates_cleared.append("STRESS_NORMALIZATION")
        
    # Gate 2: Macro Confirmation
    # Requirement: Regime must be NEUTRAL or better (score < 0.66)
    if regime_score < 0.66:
        gates_cleared.append("MACRO_CONFIRMATION")
        
    # Gate 3: Sentiment Capitulation
    # Requirement: Retail Sentiment Score < 0.30 (Contrarian "fear" signal)
    if retail_sentiment_score < 0.30:
        gates_cleared.append("SENTIMENT_CAPITULATION")
        
    is_fully_cleared = len(gates_cleared) == 3
    
    # Calculate VARES Multiplier
    # If not cleared, multiplier is 0.0. If cleared, it follows the tranche.
    vares_multiplier = 0.0
    next_tranche = current_tranche_level
    next_date = None
    
    if is_fully_cleared:
        # Check cooldown
        can_deploy = True
        if last_tranche_deployed_at:
            delta = datetime.datetime.now(datetime.timezone.utc) - last_tranche_deployed_at
            if delta.days < TRANCHE_COOLDOWN_DAYS:
                can_deploy = False
                next_date = (last_tranche_deployed_at + datetime.timedelta(days=TRANCHE_COOLDOWN_DAYS)).isoformat()
        
        if can_deploy and current_tranche_level < 4:
            next_tranche += 1
            vares_multiplier = REENTRY_TRANCHES[next_tranche]
        else:
            vares_multiplier = REENTRY_TRANCHES.get(current_tranche_level, 0.0)
            
    status = AresStatus(
        gates_cleared=gates_cleared,
        is_fully_cleared=is_fully_cleared,
        current_tranche_level=next_tranche,
        vares_multiplier=vares_multiplier,
        next_tranche_available_at=next_date
    )
    
    # Log re-entry signals
    if is_fully_cleared and vares_multiplier > 0:
        append_to_log(SessionLogEntry(
            timestamp=status.timestamp,
            action_type='ARES_REENTRY',
            triggering_module='ARES',
            triggering_signal=f"Gate 3 Clear. Deploying Tranche {next_tranche} ({vares_multiplier:.0%})",
            regime_at_action=current_regime
        ))
        
    return status

if __name__ == '__main__':
    print("ARMS ARES Module Active (Simulation Mode)")
    
    # Simulate a recovery scenario
    last_deployment = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=10)
    
    res = run_ares_check(
        current_regime="NEUTRAL",
        regime_score=0.55,
        macro_stress_score=0.35, # Gate 1 Pass
        retail_sentiment_score=0.25, # Gate 3 Pass
        last_tranche_deployed_at=last_deployment,
        current_tranche_level=1 # Already at 25%
    )
    
    print(f"ARES Status: {res}")
