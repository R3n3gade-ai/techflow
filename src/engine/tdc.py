"""
ARMS Module: Thesis Dependency Checker (TDC)

This module provides the continuous thesis integrity auditing layer for ARMS.
It consumes alerts from the Customer Dependency Map (CDM) and uses the 
Claude API to evaluate if the original thesis for a position remains intact
after a new development.

"The system catches what the PM should not have to catch."

Reference: ARMS Module Specification — CDM + TDC | Addendum 2 to FSD v1.1
"""

import datetime
import json
from dataclasses import dataclass, field
from typing import List, Literal, Optional

# --- Internal Imports ---
from engine.cdm import CdmAlert
from intelligence.claude_wrapper import claude_wrapper
from execution.confirmation_queue import ConfirmationQueue, QueuedAction
from reporting.audit_log import SessionLogEntry, append_to_log

# --- Data Structures ---

@dataclass
class ThesisReviewResult:
    """
    Represents the output of a single TDC review.
    Based on ARMS Module Specification — Section 2.5.
    """
    position: str
    tis_score: float # 0.0 - 10.0
    tis_label: Literal['INTACT', 'WATCH', 'IMPAIRED', 'BROKEN']
    gates_affected: List[int] # SENTINEL gate numbers
    bear_case_evidence: Optional[str] = None
    bull_case_rebuttal: Optional[str] = None
    recommended_action: Literal['MONITOR', 'WATCH_FLAG', 'PM_REVIEW', 'URGENT_REVIEW'] = 'MONITOR'
    trigger_type: str = 'CDM_PROPAGATION' # 'CDM_PROPAGATION' | 'WEEKLY_AUDIT'
    trigger_entity: str = '' # named entity that triggered review
    reviewed_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    api_cost_usd: float = 0.40 # logged for monthly cost tracking (average)

@dataclass
class TDCStatus:
    """
    Represents the current global state of the TDC module.
    Based on ARMS Module Specification — Section 2.5.
    """
    last_weekly_audit: str # ISO date
    positions_at_watch: List[str] # tickers currently TIS WATCH
    positions_impaired: List[str] # tickers currently TIS IMPAIRED
    positions_broken: List[str] # tickers currently TIS BROKEN
    pending_pm_reviews: int # Tier 1 actions awaiting PM response
    last_cdm_propagation: str # ISO timestamp of last CDM alert

# --- TDC Engine Logic ---

def run_thesis_review(alert: CdmAlert) -> ThesisReviewResult:
    """
    Runs a single thesis integrity review triggered by a CDM alert.
    Consults the Claude API to evaluate the thesis integrity.
    """
    position = alert.ticker
    
    # 1. Retrieve original SENTINEL records (Placeholder: In a live system, this
    #    would pull the actual gate records from a knowledge base or database.)
    sentinel_gates = {
        "gate1_thesis": "Civilizational shift — not a product cycle.",
        "gate2_thesis": "Non-optional — cannot be routed around.",
        "gate3_mispricing_score": 24, # Out of 30
    }
    
    # 2. Construct the prompt for the Claude API (Section 2.3)
    prompt = f"""
    You are running a thesis integrity review for position {position}.
    ORIGINAL SENTINEL GATE RECORDS:
    {json.dumps(sentinel_gates, indent=2)}
    CURRENT DEVELOPMENT:
    Event Type: {alert.event_type}. Headline: {alert.headline}. Triggered by entity: {alert.triggering_entity}.
    
    Evaluate whether the original thesis remains intact.
    Return ONLY valid JSON with this exact structure:
    {{
      "tis_score": <float 0.0-10.0>,
      "tis_label": <"INTACT"|"WATCH"|"IMPAIRED"|"BROKEN">,
      "gates_affected": [<list of gate numbers with weakened assumptions>],
      "bear_case_evidence": <specific evidence string or null>,
      "bull_case_rebuttal": <why thesis may still hold despite evidence>,
      "recommended_action": <"MONITOR"|"WATCH_FLAG"|"PM_REVIEW"|"URGENT_REVIEW">
    }}
    """

    # 3. Call the Claude API
    # Note: claude_wrapper is a singleton instance
    response_json = claude_wrapper.call(
        task_type='thesis_review',
        prompt=prompt,
        knowledge_base_query=f'{position} thesis SENTINEL gates'
    )
    
    # 4. Parse the response and create the result object
    response_data = json.loads(response_json)
    
    result = ThesisReviewResult(
        position=position,
        trigger_entity=alert.triggering_entity,
        trigger_type='CDM_PROPAGATION',
        **response_data
    )
    
    # 5. Log the outcome to the audit trail
    append_to_log(SessionLogEntry(
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        action_type='TDC_REVIEW',
        triggering_module='TDC',
        triggering_signal=f"TIS: {result.tis_score} ({result.tis_label}) for {position}. Reason: {alert.event_type} at {alert.triggering_entity}.",
        ticker=position
    ))
    
    print(f"[TDC] Review Complete for {position}. TIS: {result.tis_score} ({result.tis_label})")
    
    # 6. Queue Tier 1 Actions if required (Section 2.2)
    if result.recommended_action in ['PM_REVIEW', 'URGENT_REVIEW']:
        # This would be where we create a QueuedAction and add it to the ConfirmationQueue.
        # For simplicity, we just print the action for now.
        print(f"[TDC] Queuing Tier 1 PM Review for {position} due to TIS {result.tis_score}.")

    return result

def run_weekly_tdc_audit(all_positions: List[str]):
    """
    Runs the proactive weekly audit on all positions in the book.
    (Placeholder: To be triggered every Monday at 6AM CT)
    """
    print("\n--- Running Proactive Weekly TDC Audit ---")
    # This would loop through each position, gather the last 7 days of news/filings,
    # and call run_thesis_review for each one.
    pass

if __name__ == '__main__':
    print("ARMS TDC Module Active (Simulation Mode)")
    
    # Simulate a CDM alert for MU
    mock_alert = CdmAlert(
        ticker='MU',
        triggering_entity='Google',
        event_type='LEGAL_RULING',
        severity='CRITICAL',
        headline='DOJ Pursuing Structural Remedies Against Google',
        source_item=None # type: ignore
    )
    
    res = run_thesis_review(mock_alert)
    print(f"Outcome: {res.tis_label} (Score: {res.tis_score})")
