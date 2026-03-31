"""
ARMS Module: Permanent Tail Risk Hedge (PTRH) Full Automation

This module provides the full, Tier-0 autonomous operation for the PTRH. It
integrates with the Coverage Adequacy Model (CAM) to determine required coverage
and executes all necessary actions (rolls, resizing, drift correction) without
human intervention.

"Silence is trust in the architecture."

Reference: ARMS Module Specification — PTRH Automation + DSHP, Section 1
Reference: ARMS Addendum 4 — Governing Principle + PTRH Coverage Adequacy Model
"""

import datetime
from dataclasses import dataclass, field
from typing import List, Literal, Optional

# --- Internal Imports ---
from engine.cam import calculate_required_notional, CamInputs
from execution.interfaces import OrderRequest
from reporting.audit_log import SessionLogEntry, append_to_log

# --- Data Structures ---

@dataclass
class OptionsPosition:
    """
    Represents a single options position in the portfolio.
    Used for tracking existing PTRH hedges.
    """
    ticker: str
    option_type: Literal['PUT', 'CALL']
    strike: float
    expiry: str  # ISO date format 'YYYY-MM-DD'
    contracts: int
    notional_value: float
    
    @property
    def dte(self) -> int:
        """Calculates the Days To Expiration (DTE)."""
        expiry_date = datetime.datetime.strptime(self.expiry, '%Y-%m-%d').date()
        return (expiry_date - datetime.date.today()).days

@dataclass
class PTRHStatus:
    """
    Represents the complete status of the PTRH module for monitoring.
    Based on ARMS Module Specification — Section 1.5.
    """
    regime: str                 # current canonical regime label
    multiplier: float           # current sizing multiplier from CAM/Regime
    target_notional_pct: float  # % of NAV in puts
    actual_notional_pct: float  # actual current coverage
    coverage_drift_pct: float   # abs(target - actual)
    nearest_expiry_dte: int     # days to expiration of nearest position
    last_roll_date: str         # ISO date of most recent roll
    dual_risk_active: bool      # PM-declared dual-risk flag
    dual_risk_standard_pct: float # override notional if dual_risk_active
    last_action: str            # 'NONE'|'ROLL'|'RESIZE'|'CORRECT_DRIFT'
    last_action_timestamp: str  # ISO format
    alerts: List[str] = field(default_factory=list)

# --- Core Execution Support ---

def _submit_ptrh_order(action: Literal['BUY_PUT', 'SELL_PUT'], 
                       notional: float, 
                       signal: str, 
                       tier: int = 0):
    """
    Standardized internal helper to submit PTRH orders via the broker API logic.
    In a real system, this would call broker_api.submit_order().
    """
    # Create the OrderRequest as defined in L5/L6 of FSD v1.1
    order = OrderRequest(
        ticker="QQQ",
        action=action,
        quantity=notional, # Simplified: Using notional for simulation/placeholder
        order_type="MARKET",
        triggering_module="PTRH",
        triggering_signal=signal,
        tier=tier
    )
    
    # Log the action immediately to the immutable audit trail
    append_to_log(SessionLogEntry(
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        action_type='TRADE',
        triggering_module='PTRH',
        triggering_signal=signal,
        ticker="QQQ",
        regime_at_action="N/A" # Would be passed in a real system
    ))
    
    # Placeholder: print to console for development visibility
    print(f"[PTRH] {action} executed for QQQ: {signal} (${notional:,.2f} notional)")
    return "order_id_123"

# --- Main Logic Module ---

def run_ptrh_module(cam_inputs: CamInputs, 
                    current_positions: List[OptionsPosition],
                    dual_risk_override_pct: Optional[float] = None) -> PTRHStatus:
    """
    Runs the full Tier-0 PTRH management logic for a single cycle.
    
    Args:
        cam_inputs: Live market and portfolio data for CAM calculation.
        current_positions: Current QQQ put positions from the broker.
        dual_risk_override_pct: Optional PM override for dual-risk scenarios.
    
    Returns:
        A PTRHStatus object for the daily monitor or dashboard.
    """
    alerts = []
    last_action = "NONE"
    
    # 1. Determine target notional using CAM
    # Note: calculate_required_notional already incorporates the Regime Multiplier.
    required_notional = calculate_required_notional(cam_inputs)
    
    # 1.1 Handle Dual-Risk Override (Tier 2 Review trigger)
    if dual_risk_override_pct is not None:
        required_notional = cam_inputs.nav * dual_risk_override_pct
    
    actual_notional = sum(p.notional_value for p in current_positions)
    target_pct = required_notional / cam_inputs.nav if cam_inputs.nav > 0 else 0
    actual_pct = actual_notional / cam_inputs.nav if cam_inputs.nav > 0 else 0
    drift = (actual_pct / target_pct) - 1 if target_pct > 0 else 0
    
    # 2. Check DTE for rolls (Priority 1)
    # Based on Section 1.1: Roll if DTE <= 30.
    roll_occurred = False
    for pos in current_positions:
        if pos.dte <= 30:
            signal = f"DTE Roll: {pos.expiry} is at {pos.dte} days. Rolling to next expiry."
            _submit_ptrh_order('SELL_PUT', pos.notional_value, signal) # Sell current
            _submit_ptrh_order('BUY_PUT', pos.notional_value, signal)  # Buy next (ATM)
            last_action = "ROLL"
            roll_occurred = True
    
    # 3. Check notional drift and auto-correct (Priority 2)
    # Based on Section 1.1: Auto-correct if drift > 5%.
    # Section 3.1 also mentions: Under-hedging (5%) vs. Over-hedging (15%).
    if not roll_occurred: # Only correct drift if we didn't just roll
        is_under_hedged = drift < -0.05
        is_over_hedged = drift > 0.15
        
        if is_under_hedged or is_over_hedged:
            delta_notional = required_notional - actual_notional
            action = 'BUY_PUT' if delta_notional > 0 else 'SELL_PUT'
            signal = f"Drift Correction: actual {actual_pct:.2%} vs target {target_pct:.2%}. Delta: ${abs(delta_notional):,.2f}"
            _submit_ptrh_order(action, abs(delta_notional), signal)
            last_action = "CORRECT_DRIFT"
    
    # 4. Prepare Status for Monitoring
    nearest_dte = min([p.dte for p in current_positions]) if current_positions else 0
    
    # Simplified multiplier extraction from the inputs (1.0 + score is an approximation)
    # In production, we'd return the actual multiplier used in cam.py
    approx_multiplier = 1.0 + cam_inputs.regime_score 

    status = PTRHStatus(
        regime=str(cam_inputs.regime_score), # Simplified for placeholder
        multiplier=approx_multiplier,
        target_notional_pct=target_pct,
        actual_notional_pct=actual_pct,
        coverage_drift_pct=drift * 100,
        nearest_expiry_dte=nearest_dte,
        last_roll_date=datetime.date.today().isoformat() if last_action == "ROLL" else "N/A",
        dual_risk_active=(dual_risk_override_pct is not None),
        dual_risk_standard_pct=dual_risk_override_pct if dual_risk_override_pct else 0.0,
        last_action=last_action,
        last_action_timestamp=datetime.datetime.now().isoformat() if last_action != "NONE" else "",
        alerts=alerts
    )
    
    return status

if __name__ == '__main__':
    print("ARMS PTRH Module Active (Simulation Mode)")
    
    # Simulate a RISK_ON scenario
    test_inputs = CamInputs(
        current_equity_pct=1.0,
        regime_score=0.25,
        fem_concentration_score=0.40,
        macro_stress_score=0.20,
        cdm_active_signals=0,
        nav=50_000_000
    )
    
    # Existing put at 35 DTE, correct sizing
    test_pos = [OptionsPosition("QQQ", "PUT", 400, "2026-05-05", 100, 600_000)]
    
    res = run_ptrh_module(test_inputs, test_pos)
    print(f"Status: {res}")
