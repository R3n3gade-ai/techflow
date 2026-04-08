"""
ARMS Reporting: Daily Monitor v2.1 (Phase 2 Update)

This module generates the definitive Daily Monitor report at 6:00 AM CT.
It aggregates data from all core ARMS modules and now includes the
Phase 2 Behavioral and Safety layers (ARES, CDF, MC-RSS, Incapacitation).

"Silence is trust in the architecture."

Reference: ARMS FSD v1.1, Section 7 & 11.3
Reference: MASTER_IMPLEMENTATION_PLAN.md (Phase 2 Complete)
"""

import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# --- Internal Imports ---
from engine.regime_probability import RegimeProbabilitySignal
from engine.tail_hedge import PTRHStatus
from engine.tdc import ThesisReviewResult
from engine.mics import MICSResult
from engine.ares import AresStatus
from engine.cdf import CDFStatus
from engine.mc_rss import RSSResult
from engine.incapacitation import IncapacitationStatus
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
    
    # Phase 1 Data
    dshp_alerts: List[Dict[str, Any]]
    cdm_alerts: List[Dict[str, Any]]
    tdc_reviews: List[ThesisReviewResult]
    mics_summary: Dict[str, MICSResult]
    
    # Phase 2 Behavioral & Safety Data
    ares_status: AresStatus
    cdf_summary: List[CDFStatus]
    retail_sentiment: RSSResult
    safety_status: IncapacitationStatus
    
    # Execution & Portfolio
    decision_queue: List[Dict[str, Any]]
    portfolio_summary: Dict[str, float]
    position_weights: Dict[str, float] = field(default_factory=dict)
    macro_inputs: Dict[str, float] = field(default_factory=dict)
    sleeve_weights: Dict[str, float] = field(default_factory=dict)
    
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
    ares_status: AresStatus,
    cdf_statuses: List[CDFStatus],
    rss_result: RSSResult,
    safety_status: IncapacitationStatus,
    nav: float,
    portfolio_summary: Optional[Dict[str, float]] = None,
    position_weights: Optional[Dict[str, float]] = None,
    macro_inputs: Optional[Dict[str, float]] = None,
    sleeve_weights: Optional[Dict[str, float]] = None,
) -> DailyMonitor:
    """
    Aggregates all module outputs into a single DailyMonitor payload.
    """
    
    # 1. Identify Decision Queue Items (Tier 1 Actions)
    # These are items that require PM review or have an open veto window.
    decision_queue = []
    
    # Add DSHP harvests to the queue
    for action in dshp_actions:
        item = action.get('item', {})
        decision_queue.append({
            "id": action.get('action_id', 'unknown'),
            "module": "DSHP",
            "item": f"Trim {item.get('ticker', 'N/A')} to target weight.",
            "rationale": action.get('rationale', 'Gain harvesting.'),
            "status": "PENDING_VETO",
            "tier": 1
        })
        
    # Add TDC reviews that require PM review
    for review in tdc_results:
        if review.recommended_action in ['PM_REVIEW', 'URGENT_REVIEW']:
            decision_queue.append({
                "id": f"tdc_{review.position}",
                "module": "TDC",
                "item": f"Evaluate {review.position} thesis integrity.",
                "rationale": f"TIS: {review.tis_score} ({review.tis_label}). {review.bear_case_evidence}",
                "status": "PENDING_RESPONSE",
                "tier": 1
            })
            
    # Add CDF Orderly Exits to the queue
    for cdf in cdf_statuses:
        if cdf.is_orderly_exit_due:
            decision_queue.append({
                "id": f"cdf_exit_{cdf.ticker}",
                "module": "CDF",
                "item": f"Orderly exit for {cdf.ticker} (Day 135).",
                "rationale": f"Underperformance persists. Multiplier at 0.60x.",
                "status": "PENDING_VETO",
                "tier": 1
            })

    # 2. Compile Portfolio Summary (L4-L5 context)
    portfolio_summary = portfolio_summary or {
        "nav": nav,
        "equity_exposure_pct": 0.0,
        "ai_sector_exposure_pct": 0.0,
        "defensive_sleeve_pct": 0.0,
        "cash_hedge_pct": 0.0
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
        ares_status=ares_status,
        cdf_summary=cdf_statuses,
        retail_sentiment=rss_result,
        safety_status=safety_status,
        decision_queue=decision_queue,
        portfolio_summary=portfolio_summary,
        position_weights=position_weights or {},
        macro_inputs=macro_inputs or {},
        sleeve_weights=sleeve_weights or {}
    )
    
    # Audit Logging for Daily Snapshots
    print(f"[DailyMonitor] Generated for {monitor.timestamp}. Queue items: {len(decision_queue)}")
    if safety_status.current_safety_tier > 0:
        print(f"[DailyMonitor] WARNING: Safety Tier {safety_status.current_safety_tier} Active.")
        
    return monitor

if __name__ == '__main__':
    print("ARMS Daily Monitor v2.1 Active (Phase 2 Implementation)")
