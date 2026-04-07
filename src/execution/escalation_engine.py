"""
ARMS Execution: Escalation Engine

Implements Escalation Rule v2: Cumulative 2.5% drawdown auto-suppress.

Reference: THB v4.0, Section 10
"""
from dataclasses import dataclass

@dataclass
class EscalationStatus:
    cumulative_intraday_loss_pct: float
    is_suppressed: bool

def run_escalation_engine(intraday_loss: float) -> EscalationStatus:
    if intraday_loss <= -0.025:
        return EscalationStatus(cumulative_intraday_loss_pct=intraday_loss, is_suppressed=True)
    return EscalationStatus(cumulative_intraday_loss_pct=intraday_loss, is_suppressed=False)
