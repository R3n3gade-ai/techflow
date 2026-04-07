"""
ARMS Engine: Kevlar Hard Limit Enforcement

Enforces the absolute concentration limits across the portfolio.
Prevents any single thesis from destroying the fund regardless of MICS score.

Reference: CODEBASE_GAME_PLAN_v2.0.md (Step 1)
"""

# Hardcoded fund limits
MAX_SINGLE_POSITION_PCT = 0.22  # 22% Max
MIN_SINGLE_POSITION_PCT = 0.03  # 3% Min for active conviction
MAX_AI_SECTOR_PCT = 0.48        # 48% Total AI Sector Cap

def apply_kevlar_limits(target_weight: float) -> float:
    """
    Caps an individual position's target weight at the Kevlar maximums.
    If a weight falls below the 3% minimum, it must either be held at 3% or retired to 0%.
    (For sizing purposes, we cap the max. Floor handling is usually left to TRP/CDF).
    """
    # Hard cap at 22%
    if target_weight > MAX_SINGLE_POSITION_PCT:
        return MAX_SINGLE_POSITION_PCT
    
    # If it's a micro-position but meant to be active, push to minimum 3%
    # If it's truly a 0.0 exit, leave it at 0.0
    if 0.0 < target_weight < MIN_SINGLE_POSITION_PCT:
        return MIN_SINGLE_POSITION_PCT
        
    return target_weight
