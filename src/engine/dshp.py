"""
ARMS Module: Defensive Sleeve Harvest Protocol (DSHP)

This module extends gain-harvesting discipline to the defensive sleeve.
It monitors defensive positions (SGOL, DBMF) for significant appreciation
and queues Tier 1 actions to trim them back to their target weights,
crystallizing gains.

Reference: ARMS Module Specification — PTRH Automation + DSHP
"""

from dataclasses import dataclass, field
from typing import List, Dict, Literal, Optional
from datetime import datetime
import sys
import os

# Add the config directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))

from dshp_config import (
    SGOL_TARGET_WEIGHT, SGOL_HARVEST_THRESHOLD, DBMF_TARGET_WEIGHT,
    DBMF_HARVEST_THRESHOLD, DBMF_DRIFT_THRESHOLD
)

# --- Placeholder Data Structures ---

@dataclass
class DefensivePosition:
    """Represents a single position in the defensive sleeve."""
    ticker: str
    current_value: float
    entry_value: float # The cost basis of the position
    current_weight: float # current_value / total_nav

# --- DSHP Data Structures ---

@dataclass
class HarvestAction:
    """Represents a single harvest action to be queued for PM review."""
    instrument: Literal['SGOL', 'DBMF']
    action_type: Literal['TRIM_TO_TARGET'] = 'TRIM_TO_TARGET'
    trim_amount_usd: float
    proceeds_to: Literal['SGOV'] = 'SGOV'
    trigger: Literal['APPRECIATION', 'WEIGHT_DRIFT']
    trigger_value: float # The % appreciation or % weight drift
    tier: Literal[1] = 1
    veto_window_hours: float = 4.0
    queued_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

# --- DSHP Engine Logic ---

def check_dshp_triggers(
    sleeve_positions: Dict[str, DefensivePosition],
    total_nav: float
) -> List[HarvestAction]:
    """
    Checks eligible defensive sleeve positions against their harvest thresholds.

    Args:
        sleeve_positions: A dict of DefensivePosition objects, keyed by ticker.
        total_nav: The total portfolio Net Asset Value.

    Returns:
        A list of HarvestAction objects for any triggered trims.
    """
    actions = []

    # 1. Check SGOL (Gold) - Appreciation Trigger
    if 'SGOL' in sleeve_positions:
        sgol = sleeve_positions['SGOL']
        appreciation = (sgol.current_value - sgol.entry_value) / sgol.entry_value
        
        if appreciation > SGOL_HARVEST_THRESHOLD:
            target_value = total_nav * SGOL_TARGET_WEIGHT
            trim_amount = sgol.current_value - target_value
            if trim_amount > 0:
                actions.append(HarvestAction(
                    instrument='SGOL',
                    trim_amount_usd=trim_amount,
                    trigger='APPRECIATION',
                    trigger_value=appreciation
                ))
                print(f"AUDIT LOG: DSHP trigger for SGOL. Appreciation {appreciation:.2%}. Queuing trim of ${trim_amount:,.2f}.")

    # 2. Check DBMF (Managed Futures) - Dual Trigger
    if 'DBMF' in sleeve_positions:
        dbmf = sleeve_positions['DBMF']
        appreciation = (dbmf.current_value - dbmf.entry_value) / dbmf.entry_value
        weight_drift = dbmf.current_weight - DBMF_TARGET_WEIGHT

        triggered = False
        trigger_type = None
        trigger_val = 0.0

        if appreciation > DBMF_HARVEST_THRESHOLD:
            triggered = True
            trigger_type = 'APPRECIATION'
            trigger_val = appreciation
        elif weight_drift > DBMF_DRIFT_THRESHOLD:
            triggered = True
            trigger_type = 'WEIGHT_DRIFT'
            trigger_val = weight_drift

        if triggered:
            target_value = total_nav * DBMF_TARGET_WEIGHT
            trim_amount = dbmf.current_value - target_value
            if trim_amount > 0:
                actions.append(HarvestAction(
                    instrument='DBMF',
                    trim_amount_usd=trim_amount,
                    trigger=trigger_type,
                    trigger_value=trigger_val
                ))
                print(f"AUDIT LOG: DSHP trigger for DBMF. Trigger: {trigger_type} ({trigger_val:.2%}). Queuing trim of ${trim_amount:,.2f}.")

    # TODO: Send any generated actions to the Tier 1 confirmation queue.
    if actions:
        print(f"ACTION: {len(actions)} harvest action(s) to be sent to confirmation queue.")

    return actions

# This file is intended to be imported as a module.
# The test cases have been moved to tests/test_dshp.py
