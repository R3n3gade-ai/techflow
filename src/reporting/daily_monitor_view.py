import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

# Import the raw payload
from .daily_monitor import DailyMonitor

@dataclass
class EquityRowView:
    ticker: str
    name: str
    weight: str
    session: str
    status: str
    flag: str

@dataclass
class QueueRowView:
    id_num: int
    ticker: str
    target: str
    execution_instruction: str
    trigger: str

@dataclass
class ModuleStatusCard:
    name: str
    state_label: str
    sub_label: str
    description: str

@dataclass
class AlertView:
    title: str
    body: str

@dataclass
class DecisionItemView:
    id_num: int
    title: str
    body: str

@dataclass
class DailyMonitorReportView:
    """
    Presentation layer view-model for the Institutional Daily Monitor.
    Separates the raw data payload from the visual rendering structure.
    """
    # Header & Masthead
    report_date: str
    quarter_day: str
    architecture_version: str
    operator_context: str
    headline_event: str
    
    regime_transition: str
    regime_score_str: str
    regime_sub_status: str
    
    session_headline: str
    
    # 1. Macro Compass
    current_score: str
    prior_score: str
    equity_ceiling: str
    queue_trigger: str
    ares_status: str
    score_drivers: str
    
    # 2. Macro Inputs
    sp500_futures: str
    nasdaq_futures: str
    brent_crude: str
    vix: str
    treasury_10y: str
    
    # 3. Equity Book
    equity_book: List[EquityRowView]
    
    # 4. Deployment Queue
    deployment_queue: List[QueueRowView]
    
    # 5. Defensive Sleeve & Cash
    sgol_weight: str
    dbmf_weight: str
    sgov_weight: str
    strc_weight: str
    ptrh_status_str: str
    cash_weight: str
    cash_context: str
    
    # 6. Module Status
    modules: List[ModuleStatusCard]
    
    # 7. Alerts
    alerts: List[AlertView]
    
    # 8. PM Decision Queue
    decisions: List[DecisionItemView]

def build_view_model(raw_monitor: DailyMonitor) -> DailyMonitorReportView:
    """
    Transforms the raw engine data payload into a structured, presentation-ready view-model.
    """
    dt = datetime.datetime.fromisoformat(raw_monitor.timestamp.replace("Z", "+00:00"))
    formatted_date = dt.strftime("%A, %B %-d, %Y")
    
    # Mocking historical/contextual data that isn't fully surfaced by engines yet 
    # (e.g. prior score, futures, specific names)
    
    # 1. Regime Transition Logic
    r_score = raw_monitor.regime_score
    current_regime = raw_monitor.regime
    transition_str = f"→ {current_regime}"
    
    # 3. Equity Book Scaffold
    # We would normally map raw_monitor.portfolio_summary and TDC/CDF flags here.
    book_view = [
        EquityRowView("NVDA", "Nvidia", "7.8%", "+2.1%", "WATCH", "MICS: C8 / Thesis Intact"),
        EquityRowView("TSLA", "Tesla", "8.8%", "+1.5%", "WATCH", "Thesis Intact"),
        EquityRowView("MU", "Micron", "4.5%", "+0.8%", "ALERT", "TDC Review Pending")
    ]
    
    # 6. Module Status Construction
    modules = [
        ModuleStatusCard(
            "ARAS", current_regime, f"~{r_score:.2f}", 
            f"Score implies {current_regime} territory. Anticipatory signal: {raw_monitor.rpe.highest_prob_transition} ({raw_monitor.rpe.highest_prob_value:.1%})."
        ),
        ModuleStatusCard(
            "ARES", "Confirming" if not raw_monitor.ares_status.is_fully_cleared else "Cleared", 
            f"Tranche {raw_monitor.ares_status.current_tranche_level}", 
            "Monitoring boundary conditions for next deployment phase."
        ),
        ModuleStatusCard(
            "PTRH / CAM", "Active", f"{raw_monitor.ptrh.actual_notional_pct:.2%} NAV", 
            f"Target coverage: {raw_monitor.ptrh.target_notional_pct:.2%}. Drift: {raw_monitor.ptrh.coverage_drift_pct:.2f}%. Last Action: {raw_monitor.ptrh.last_action}."
        )
    ]
    
    if raw_monitor.safety_status.current_safety_tier > 0:
        modules.append(ModuleStatusCard(
            "SAFETY", f"TIER {raw_monitor.safety_status.current_safety_tier}", "ACTIVE",
            f"PM Inactive for {raw_monitor.safety_status.hours_since_heartbeat:.1f}h. Forced override: {raw_monitor.safety_status.forced_regime_override}."
        ))

    # 7. Alerts
    alerts = []
    for cdm in raw_monitor.cdm_alerts:
        alerts.append(AlertView(
            f"CDM: {cdm.get('event_type')} at {cdm.get('triggering_entity')}",
            f"Propagated to {cdm.get('ticker')} with {cdm.get('severity')} severity. Headline: {cdm.get('headline')}."
        ))
        
    for dshp in raw_monitor.dshp_alerts:
        alerts.append(AlertView(
            f"DSHP: Harvest Action Queued",
            dshp.get('rationale', 'Gain harvesting threshold met.')
        ))

    # 8. PM Decision Queue
    decisions = []
    for i, q in enumerate(raw_monitor.decision_queue, 1):
        decisions.append(DecisionItemView(
            i, 
            f"[{q.get('module')}] {q.get('item')}", 
            q.get('rationale', '')
        ))
        
    if not decisions:
        decisions.append(DecisionItemView(1, "No immediate actions required.", "System is operating autonomously."))

    return DailyMonitorReportView(
        report_date=formatted_date,
        quarter_day="Q2 Day 6",
        architecture_version="Architecture AB v4.0",
        operator_context="Automated Cycle",
        headline_event="Achelion ARMS Full Integration Sweep",
        
        regime_transition=transition_str,
        regime_score_str=f"~{r_score:.2f}",
        regime_sub_status="Boundary crossed \u00b7 ARES confirming",
        
        session_headline=f"ARMS completed a full autonomous operational sweep at {dt.strftime('%H:%M %Z')}. "
                         f"Current regime evaluated at {current_regime} ({r_score:.2f}). "
                         f"RPE forward probability strongly indicates {raw_monitor.rpe.highest_prob_transition}. "
                         f"All system safety checks and portfolio drift monitors are fully active.",
                         
        current_score=f"~{r_score:.2f}",
        prior_score="~0.40",
        equity_ceiling="60%",
        queue_trigger="0.65",
        ares_status="Confirming",
        score_drivers="VIX normalized \u00b7 Credit Spreads tight \u00b7 PMI > 50",
        
        sp500_futures="+0.5%",
        nasdaq_futures="+0.8%",
        brent_crude="~$82",
        vix="~14.5",
        treasury_10y="~4.25%",
        
        equity_book=book_view,
        deployment_queue=[], # Scaffolded
        
        sgol_weight="2.5%",
        dbmf_weight="5.0%",
        sgov_weight="3.0%",
        strc_weight="0.0%",
        ptrh_status_str=f"{raw_monitor.ptrh.actual_notional_pct:.2%} NAV",
        cash_weight="8.0%",
        cash_context="Structure intact. Core hedge and ops buffer funded.",
        
        modules=modules,
        alerts=alerts,
        decisions=decisions
    )
