"""
ARMS Engine: PERM (Covered Call Execution)

Executes covered calls against core equity positions to harvest yield
when conviction decays or targets are reached. Tied to TRP.

Reference: THB v4.0, Section 10
"""
from dataclasses import dataclass
from typing import List
from execution.order_request import OrderRequest
from engine.thesis_retirement import TRPStatus

@dataclass
class PermStatus:
    active_overwrites: int
    yield_harvested_usd: float

def run_perm_evaluation(trp_statuses: List[TRPStatus]) -> List[OrderRequest]:
    orders = []
    for trp in trp_statuses:
        # If position is decaying but not fully broken, overwrite it
        if trp.cdf_multiplier <= 0.80 and not trp.is_retirement_due:
            # Generate SELL_CALL order request
            orders.append(OrderRequest(
                ticker=trp.ticker,
                action='SELL_CALL',
                quantity=1.0, # 1 contract per 100 shares approximation
                order_type='LIMIT',
                limit_price=0.50, # Placeholder premium
                execution_window_min=60,
                slippage_budget_bps=10.0,
                priority=3,
                triggering_module='PERM',
                triggering_signal=f"PERM Overwrite due to CDF decay ({trp.cdf_multiplier}x)",
                tier=1,
                confirmation_required=True,
                veto_window_hours=4.0
            ))
    return orders
