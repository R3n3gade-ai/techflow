"""
ARMS Reporting: Proactive Intelligence Digest (PID)

This module automates the generation of the monthly LP report. It leverages the 
Claude API to synthesize session logs, performance data, and SENTINEL analyses 
into a professional, defensible narrative that builds long-term investor trust.

"Transparency as competitive advantage."

Reference: ARMS FSD v1.1, Section 5.4 & 11.3
Reference: ARMS Intelligence Architecture Addendum 3, Section 5.2
"""

import datetime
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# --- Internal Imports ---
from intelligence.claude_wrapper import claude_wrapper
from reporting.audit_log import SessionLogEntry

# --- Data Structures ---

@dataclass
class LPReport:
    """The final monthly report payload."""
    month: str
    year: int
    executive_summary: str
    regime_history_narrative: str
    top_theses_summary: str
    risk_management_audit: str
    generated_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

# --- PID Logic ---

class ProactiveIntelligenceDigest:
    """
    Synthesizes monthly system data into investor-ready narratives.
    """

    def __init__(self, log_path: str = "achelion_arms/logs/session_log.jsonl"):
        self.log_path = log_path

    def _get_monthly_stats(self) -> Dict[str, Any]:
        """
        Aggregates data from the audit log for the current month.
        Placeholder for actual log parsing logic.
        """
        return {
            "regime_transitions": 2,
            "total_trades": 14,
            "sentinel_scans": 156,
            "new_positions": 2,
            "avg_mics_score": 7.4,
            "pds_triggers": 0
        }

    def generate_monthly_report(self, month: str, year: int) -> LPReport:
        """
        Runs the full AI-driven synthesis for the monthly digest.
        """
        print(f"[PID] Generating Proactive Intelligence Digest for {month} {year}...")
        
        stats = self._get_monthly_stats()
        
        # 1. Construct the Narrative Prompt for Claude
        prompt = f"""
        You are the Investor Relations Lead for Achelion Capital. 
        Synthesize the following system activity for {month} {year} into a professional LP report.
        
        MONTHLY STATS:
        {json.dumps(stats, indent=2)}
        
        REPORT REQUIREMENTS:
        1. Executive Summary: Focus on the transition from human-managed to autonomous risk.
        2. Regime History: Explain why the system stayed in or transitioned between regimes.
        3. Top Theses: Highlight the top 2 SENTINEL-approved positions.
        4. Risk Audit: Reassure LPs that PDS and PTRH are active and disciplined.
        
        STYLE: Institutional, transparent, data-driven, and confident.
        """
        
        # 2. Call Claude API for Narrative Generation
        response_json = claude_wrapper.call(
            task_type='lp_narrative',
            prompt=prompt,
            knowledge_base_query=f'Achelion monthly activity {month} {year}'
        )
        
        # Note: In a production run, we'd parse a structured JSON from Claude.
        # For simulation, we return the synthesized sections.
        
        report = LPReport(
            month=month,
            year=year,
            executive_summary="This month marked a milestone in execution autonomy...",
            regime_history_narrative=f"The system managed {stats['regime_transitions']} transitions...",
            top_theses_summary="Our SENTINEL scans identified high-conviction opportunities in...",
            risk_management_audit="PTRH remains fully optimized with zero human overrides required..."
        )
        
        # 3. Save Report for PM Review (Tier 2)
        self._save_report(report)
        
        print(f"[PID] Report generated and queued for Tier 2 PM approval.")
        return report

    def _save_report(self, report: LPReport):
        """Saves the report to the docs directory for review."""
        filename = f"achelion_arms/docs/LP_REPORT_{report.month}_{report.year}.json"
        with open(filename, 'w') as f:
            json.dump(report.__dict__, f, indent=4)

if __name__ == '__main__':
    pid = ProactiveIntelligenceDigest()
    pid.generate_monthly_report("March", 2026)
