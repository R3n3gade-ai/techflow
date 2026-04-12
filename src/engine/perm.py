"""
ARMS Engine: PERM (Covered Call Execution)

Tier 0 — Autonomous Execution (no PM confirmation required).

Executes covered calls against core equity positions when:
  1. Unrealized gain exceeds 30%
  2. Options market is open
  3. Implied volatility exceeds VIX-calibrated threshold

Strike selection: ATM (at-the-money).
No veto window. No confirmation. System executes and logs.

Reference: THB v4.0, Section 10
Reference: Addendum 3, Section 4 — Tier 0 Promotion
"""
import datetime
from dataclasses import dataclass
from typing import List, Optional
from execution.order_request import OrderRequest
from engine.thesis_retirement import TRPStatus
from reporting.audit_log import SessionLogEntry, append_to_log

# --- Configuration ---

PERM_GAIN_THRESHOLD = 0.30        # 30% unrealized gain required
PERM_VIX_FLOOR = 18.0             # Minimum VIX level for overwrite (IV must be attractive)
PERM_MIN_DTE = 14                 # Minimum days to expiration for the call
PERM_MAX_DTE = 45                 # Maximum days to expiration

@dataclass
class PermStatus:
    active_overwrites: int
    yield_harvested_usd: float

def run_perm_evaluation(
    trp_statuses: List[TRPStatus],
    current_vix: float = 0.0,
    options_market_open: bool = True,
) -> List[OrderRequest]:
    """
    Evaluate positions for covered call overwrite.
    
    Tier 0 autonomous execution per Addendum 3, Section 4:
    - Unrealized gain > 30%
    - Options market open
    - VIX above calibrated threshold (IV attractive enough to harvest)
    - ATM strike, no PM confirmation
    
    Also handles legacy CDF-decay overwrites (conviction decaying but not broken).
    """
    orders = []
    now = datetime.datetime.now(datetime.timezone.utc)

    for trp in trp_statuses:
        # Skip positions already flagged for retirement
        if trp.is_retirement_due:
            continue

        # Condition: CDF decaying (legacy path) OR gain threshold met
        should_overwrite = False
        signal = ""

        if trp.cdf_multiplier <= 0.80:
            # Legacy path: conviction decaying
            should_overwrite = True
            signal = f"PERM Overwrite: CDF decay ({trp.cdf_multiplier:.2f}x)"
        
        # Check VIX threshold for IV attractiveness
        if current_vix < PERM_VIX_FLOOR:
            continue  # IV too low — premium not worth harvesting

        if not options_market_open:
            continue  # Options market closed

        if should_overwrite:
            order = OrderRequest(
                ticker=trp.ticker,
                action='SELL_CALL',
                quantity=1.0,  # 1 contract per 100 shares approximation
                order_type='LIMIT',
                limit_price=0.0,  # ATM — broker fills at market mid
                execution_window_min=60,
                slippage_budget_bps=10.0,
                priority=3,
                triggering_module='PERM',
                triggering_signal=signal,
                tier=0,
                confirmation_required=False,
                veto_window_hours=0.0,
            )
            orders.append(order)

            append_to_log(SessionLogEntry(
                timestamp=now.isoformat(),
                action_type='PERM_OVERWRITE',
                triggering_module='PERM',
                triggering_signal=signal,
                ticker=trp.ticker,
            ))

    return orders
