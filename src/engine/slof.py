"""
ARMS Engine: Synthetic Leverage Overlay Facility (SLOF)

Governs the expansion of portfolio exposure above 100% NAV using 
synthetic instruments when AUP conditions are met.

Reference: THB v4.0, Section 10
"""
from dataclasses import dataclass
from engine.asymmetric_upside import AupStatus

@dataclass
class SlofStatus:
    is_active: bool
    current_leverage_ratio: float
    target_leverage_ratio: float

def run_slof_manager(aup_status: AupStatus, current_leverage: float) -> SlofStatus:
    if aup_status.is_expansion_eligible:
        target = aup_status.slof_multiplier # e.g., 1.25x
        active = True
    else:
        target = 1.00 # Delever to 1.0x
        active = False
        
    return SlofStatus(
        is_active=active,
        current_leverage_ratio=current_leverage,
        target_leverage_ratio=target
    )
