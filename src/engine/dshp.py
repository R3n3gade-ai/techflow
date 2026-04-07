"""
ARMS Module: Defensive Sleeve Harvest Protocol (DSHP)

This module extends gain-harvesting discipline to the defensive sleeve.
It monitors defensive positions (SGOL, DBMF) for significant appreciation
and queues Tier 1 actions to trim them back to their target weights,
crystallizing gains.

"Silence is trust in the architecture."

Reference: ARMS Module Specification — PTRH Automation + DSHP, Section 2
"""

import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Literal, Optional

# --- Internal Imports ---
from config.dshp_config import (
    SGOL_TARGET_WEIGHT, SGOL_HARVEST_THRESHOLD, 
    DBMF_TARGET_WEIGHT, DBMF_HARVEST_THRESHOLD, DBMF_DRIFT_THRESHOLD,
    DSHP_VETO_WINDOW_HOURS
)
from execution.order_request import OrderRequest
from execution.confirmation_queue import QueuedAction
from reporting.audit_log import SessionLogEntry, append_to_log

# --- Data Structures ---

@dataclass
class DefensivePosition:
    """Represents a single position in the defensive sleeve."""
    ticker: str
    current_value: float
    entry_value: float    # Cost basis
    current_weight: float  # current_value / total_nav

# --- DSHP Core Logic ---

def run_dshp_check(sleeve_positions: Dict[str, DefensivePosition], 
                   total_nav: float) -> List[QueuedAction]:
    """
    Checks defensive sleeve positions against harvest thresholds and 
    returns a list of Tier 1 actions to be queued for PM review.
    
    Args:
        sleeve_positions: Dict of DefensivePosition objects, keyed by ticker.
        total_nav: Total portfolio Net Asset Value.
        
    Returns:
        List of QueuedAction objects for any triggered trims.
    """
    queued_actions = []
    timestamp_str = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M')

    # 1. Check SGOL (Gold) - Appreciation Trigger (>20%)
    if 'SGOL' in sleeve_positions:
        sgol = sleeve_positions['SGOL']
        appreciation = (sgol.current_value - sgol.entry_value) / sgol.entry_value
        
        if appreciation > SGOL_HARVEST_THRESHOLD:
            target_value = total_nav * SGOL_TARGET_WEIGHT
            trim_amount = sgol.current_value - target_value
            
            if trim_amount > 0:
                # Create OrderRequest for the trim
                order = OrderRequest(
                    ticker='SGOL',
                    action='SELL',
                    quantity=trim_amount, # Transitional semantics: USD notional placeholder
                    order_type='MARKET',
                    execution_window_min=30,
                    slippage_budget_bps=8.0,
                    priority=3,
                    triggering_module='DSHP',
                    triggering_signal=f"Appreciation Harvest: {appreciation:.2%} (Target 2.0%)",
                    tier=1,
                    confirmation_required=True,
                    veto_window_hours=DSHP_VETO_WINDOW_HOURS
                )
                
                # Wrap in QueuedAction for Tier 1 Veto Window
                action = QueuedAction(
                    action_id=f"dshp_sgol_{timestamp_str}",
                    item=order,
                    triggering_module='DSHP',
                    rationale=order.triggering_signal,
                    queued_at=datetime.datetime.now(datetime.timezone.utc),
                    veto_window_hours=DSHP_VETO_WINDOW_HOURS
                )
                queued_actions.append(action)
                
                # Log the trigger to the audit trail
                append_to_log(SessionLogEntry(
                    timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    action_type='DSHP_TRIGGER',
                    triggering_module='DSHP',
                    triggering_signal=order.triggering_signal,
                    ticker='SGOL'
                ))

    # 2. Check DBMF (Managed Futures) - Dual Trigger (>15% app or >1.5pp drift)
    if 'DBMF' in sleeve_positions:
        dbmf = sleeve_positions['DBMF']
        appreciation = (dbmf.current_value - dbmf.entry_value) / dbmf.entry_value
        weight_drift = dbmf.current_weight - DBMF_TARGET_WEIGHT
        
        triggered = False
        signal = ""
        
        if appreciation > DBMF_HARVEST_THRESHOLD:
            triggered = True
            signal = f"Appreciation Harvest: {appreciation:.2%} (Target 5.0%)"
        elif weight_drift > DBMF_DRIFT_THRESHOLD:
            triggered = True
            signal = f"Weight Drift Harvest: {dbmf.current_weight:.2%} (Target 5.0%)"
            
        if triggered:
            target_value = total_nav * DBMF_TARGET_WEIGHT
            trim_amount = dbmf.current_value - target_value
            
            if trim_amount > 0:
                order = OrderRequest(
                    ticker='DBMF',
                    action='SELL',
                    quantity=trim_amount, # Transitional semantics: USD notional placeholder
                    order_type='MARKET',
                    execution_window_min=30,
                    slippage_budget_bps=8.0,
                    priority=3,
                    triggering_module='DSHP',
                    triggering_signal=signal,
                    tier=1,
                    confirmation_required=True,
                    veto_window_hours=DSHP_VETO_WINDOW_HOURS
                )
                
                action = QueuedAction(
                    action_id=f"dshp_dbmf_{timestamp_str}",
                    item=order,
                    triggering_module='DSHP',
                    rationale=signal,
                    queued_at=datetime.datetime.now(datetime.timezone.utc),
                    veto_window_hours=DSHP_VETO_WINDOW_HOURS
                )
                queued_actions.append(action)
                
                append_to_log(SessionLogEntry(
                    timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    action_type='DSHP_TRIGGER',
                    triggering_module='DSHP',
                    triggering_signal=signal,
                    ticker='DBMF'
                ))

    return queued_actions

if __name__ == '__main__':
    print("ARMS DSHP Module Active (Simulation Mode)")
    
    # Simulate a drift in DBMF
    mock_nav = 50_000_000
    mock_positions = {
        'DBMF': DefensivePosition(
            ticker='DBMF',
            current_value=mock_nav * 0.07, # 7.0% weight (2.0pp drift)
            entry_value=mock_nav * 0.05,
            current_weight=0.07
        )
    }
    
    actions = run_dshp_check(mock_positions, mock_nav)
    for a in actions:
        print(f"Queued: {a.action_id} - {a.rationale}")
