"""
ARMS Reporting: Daily Monitor v2.0

This module generates the definitive Daily Monitor report at 6:00 AM CT.
It aggregates data from all core ARMS modules (ARAS, MICS, PTRH, DSHP, CDM, TDC, RPE)
and prepares it for the PM Control Room dashboard.

"Silence is trust in the architecture."

Reference: ARMS FSD v1.1, Section 7 & 11.3
Reference: monitor_examples/ (Visual Specification)
"""

import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# --- Internal Imports ---
from engine.regime_probability import RegimeProbabilitySignal
from engine.tail_hedge import PTRHStatus
from engine.tdc import ThesisReviewResult
from engine.mics import MICSResult
from reporting.audit_log import SessionLogEntry

# --- Data Structures ---

@dataclass
class DailyMonitor:
    """The complete data payload for the Daily Monitor dashboard."""
    timestamp: str
    regime: str
    regime_score: float
    rpe: RegimeProbabilitySignal
    ptrh: PTRHStatus
    dshp_alerts: List[Dict[str, Any]]
    cdm_alerts: List[Dict[str, Any]]
    tdc_reviews: List[ThesisReviewResult]
    mics_summary: Dict[str, MICSResult]
    decision_queue: List[Dict[str, Any]]
    portfolio_summary: Dict[str, float]
    
# --- Monitor Generation Logic ---

def generate_daily_monitor(
    current_regime: str,
    regime_score: float,
    rpe_signal: RegimeProbabilitySignal,
    ptrh_status: PTRHStatus,
    mics_results: Dict[str, MICSResult],
    tdc_results: List[ThesisReviewResult],
    cdm_alerts: List[Dict[str, Any]],
    dshp_actions: List[Dict[str, Any]],
    nav: float
) -> DailyMonitor:
    """
    Aggregates all module outputs into a single DailyMonitor payload.
    """
    
    # 1. Identify Decision Queue Items (Tier 1 Actions)
    # These are items that require PM review or have an open veto window.
    decision_queue = []
    
    # Add DSHP harvests to the queue
    for action in dshp_actions:
        decision_queue.append({
            "id": action['action_id'],
            "type": "DSHP_HARVEST",
            "item": f"Trim {action['instrument']} to target weight.",
            "rationale": action['rationale'],
            "status": "PENDING_VETO",
            "tier": 1
        })
        
    # Add TDC reviews that require PM review
    for review in tdc_results:
        if review.recommended_action in ['PM_REVIEW', 'URGENT_REVIEW']:
            decision_queue.append({
                "id": f"tdc_{review.position}",
                "type": "THESIS_REVIEW",
                "item": f"Evaluate {review.position} thesis integrity.",
                "rationale": f"TIS: {review.tis_score} ({review.tis_label}). {review.bear_case_evidence}",
                "status": "PENDING_RESPONSE",
                "tier": 1
            })

    # 2. Compile Portfolio Summary (L4-L5 context)
    portfolio_summary = {
        "nav": nav,
        "equity_exposure_pct": 0.58, # Placeholder
        "ai_sector_exposure_pct": 0.20,
        "defensive_sleeve_pct": 0.14,
        "cash_hedge_pct": 0.08
    }

    # 3. Finalize the Monitor Payload
    monitor = DailyMonitor(
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        regime=current_regime,
        regime_score=regime_score,
        rpe=rpe_signal,
        ptrh=ptrh_status,
        dshp_alerts=dshp_actions,
        cdm_alerts=cdm_alerts,
        tdc_reviews=tdc_results,
        mics_summary=mics_results,
        decision_queue=decision_queue,
        portfolio_summary=portfolio_summary
    )
    
    # Audit Logging
    print(f"[DailyMonitor] Generated for {monitor.timestamp}. Queue items: {len(decision_queue)}")
    return monitor

if __name__ == '__main__':
    print("ARMS Daily Monitor Generator Active")
    # Simulation would go here
