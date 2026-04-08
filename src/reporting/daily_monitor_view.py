import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

from engine.aras import calculate_aras_ceiling

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
    Only sourced values should appear here; unknowns are labeled explicitly.
    """
    dt = datetime.datetime.fromisoformat(raw_monitor.timestamp.replace("Z", "+00:00"))
    formatted_date = dt.strftime("%A, %B %-d, %Y")

    r_score = raw_monitor.regime_score
    current_regime = raw_monitor.regime
    transition_str = f"→ {current_regime}"
    aras_output = calculate_aras_ceiling(r_score)

    nav = float(raw_monitor.portfolio_summary.get("nav", 0.0) or 0.0)
    equity_exposure = float(raw_monitor.portfolio_summary.get("equity_exposure_pct", 0.0) or 0.0)
    defensive_sleeve = float(raw_monitor.portfolio_summary.get("defensive_sleeve_pct", 0.0) or 0.0)
    cash_hedge = float(raw_monitor.portfolio_summary.get("cash_hedge_pct", 0.0) or 0.0)

    book_view: List[EquityRowView] = []
    tdc_by_ticker = {r.position: r for r in raw_monitor.tdc_reviews}
    for ticker, mics in sorted(raw_monitor.mics_summary.items()):
        conviction = getattr(mics, 'conviction_level', 'N/A')
        review = tdc_by_ticker.get(ticker)
        weight = raw_monitor.position_weights.get(ticker)
        weight_str = f"{weight:.1%}" if weight is not None else "N/A"
        if review:
            status = review.tis_label
            flag = f"MICS C{conviction} · TIS {review.tis_score:.1f} {review.tis_label}"
            session_text = review.recommended_action
        else:
            status = "WATCH" if conviction != 'N/A' and conviction >= 5 else "ALERT"
            flag = f"MICS C{conviction} · No active TDC review"
            session_text = "MONITOR"
        book_view.append(EquityRowView(ticker, ticker, weight_str, session_text, status, flag))

    queue_view: List[QueueRowView] = []
    strategic_queue = [q for q in raw_monitor.decision_queue if q.get('module') in {'DSHP', 'CDF', 'TDC'}]
    for i, q in enumerate(strategic_queue, 1):
        status = q.get('status', 'PENDING')
        queue_view.append(QueueRowView(
            id_num=i,
            ticker=q.get('module', 'N/A'),
            target=status.replace('_', ' '),
            execution_instruction=q.get('item', 'N/A'),
            trigger=q.get('rationale', 'N/A')
        ))

    modules = [
        ModuleStatusCard(
            "ARAS", current_regime, f"~{r_score:.2f}",
            f"Sourced regime score. RPE signal: {raw_monitor.rpe.highest_prob_transition} ({raw_monitor.rpe.highest_prob_value:.1%})."
        ),
        ModuleStatusCard(
            "ARES",
            "Cleared" if raw_monitor.ares_status.is_fully_cleared else "Confirming",
            f"Tranche {raw_monitor.ares_status.current_tranche_level} · VARES {raw_monitor.ares_status.vares_multiplier:.0%}",
            (
                "Re-entry gates cleared: " + ", ".join(raw_monitor.ares_status.gates_cleared)
                if raw_monitor.ares_status.gates_cleared else
                "Awaiting full re-entry gate clearance."
            )
        ),
        ModuleStatusCard(
            "PTRH / CAM", "Active", f"{raw_monitor.ptrh.actual_notional_pct:.2%} NAV",
            f"Target {raw_monitor.ptrh.target_notional_pct:.2%}; drift {raw_monitor.ptrh.coverage_drift_pct:.2f}% ; last action {raw_monitor.ptrh.last_action}."
        ),
        ModuleStatusCard(
            "TDC", "Active" if raw_monitor.tdc_reviews else "Idle",
            f"{len(raw_monitor.tdc_reviews)} review(s)",
            "Continuous thesis integrity auditing from CDM propagations."
        ),
        ModuleStatusCard(
            "CDM", "Active" if raw_monitor.cdm_alerts else "Quiet",
            f"{len(raw_monitor.cdm_alerts)} propagated alert(s)",
            "Named-entity dependency propagation layer."
        ),
        ModuleStatusCard(
            "MC-RSS", raw_monitor.retail_sentiment.signal_label,
            f"{raw_monitor.retail_sentiment.composite_rss:.2f}",
            "Retail sentiment contrarian overlay."
        )
    ]

    cdf_due = [c for c in raw_monitor.cdf_summary if c.is_orderly_exit_due]
    modules.append(ModuleStatusCard(
        "CDF",
        "Exit Due" if cdf_due else "Monitoring",
        f"{len(raw_monitor.cdf_summary)} tracked / {len(cdf_due)} due",
        "Conviction decay and orderly exit discipline layer."
    ))

    if raw_monitor.safety_status.current_safety_tier > 0:
        modules.append(ModuleStatusCard(
            "SAFETY", f"TIER {raw_monitor.safety_status.current_safety_tier}", "ACTIVE",
            f"PM inactive for {raw_monitor.safety_status.hours_since_heartbeat:.1f}h. Forced override: {raw_monitor.safety_status.forced_regime_override}."
        ))

    alerts: List[AlertView] = []
    for cdm in raw_monitor.cdm_alerts:
        alerts.append(AlertView(
            f"CDM: {cdm.get('event_type')} at {cdm.get('triggering_entity')}",
            f"Propagated to {cdm.get('ticker')} with {cdm.get('severity')} severity. Headline: {cdm.get('headline')}."
        ))
    for dshp in raw_monitor.dshp_alerts:
        alerts.append(AlertView(
            "DSHP: Harvest Action Queued",
            dshp.get('rationale', 'Gain harvesting threshold met.')
        ))
    for review in raw_monitor.tdc_reviews:
        alerts.append(AlertView(
            f"TDC: {review.position} {review.tis_label}",
            f"TIS {review.tis_score:.1f}. Trigger: {review.trigger_entity or 'N/A'}. {review.bear_case_evidence or review.bull_case_rebuttal or 'No thesis detail returned.'}"
        ))
    if not alerts:
        alerts.append(AlertView("No sourced alerts", "No new live alerts fired in this cycle."))

    decisions = []
    for i, q in enumerate(raw_monitor.decision_queue, 1):
        status = q.get('status', 'PENDING').replace('_', ' ')
        decisions.append(DecisionItemView(i, f"[{q.get('module')}] {q.get('item')} ({status})", q.get('rationale', '')))
    if not decisions:
        decisions.append(DecisionItemView(1, "No immediate actions required.", "No Tier 1 items were generated from sourced inputs."))

    return DailyMonitorReportView(
        report_date=formatted_date,
        quarter_day="LIVE CYCLE",
        architecture_version="Architecture AB v4.0",
        operator_context="Automated Cycle",
        headline_event="Sourced ARMS operational sweep",
        regime_transition=transition_str,
        regime_score_str=f"~{r_score:.2f}",
        regime_sub_status="Sourced from live cycle state",
        session_headline=(
            f"ARMS completed an operational sweep at {dt.strftime('%H:%M %Z')}. "
            f"Current regime: {current_regime} ({r_score:.2f}). "
            f"Portfolio NAV ${nav:,.2f}. "
            f"CDM alerts: {len(raw_monitor.cdm_alerts)} · TDC reviews: {len(raw_monitor.tdc_reviews)} · Decision queue: {len(raw_monitor.decision_queue)}."
        ),
        current_score=f"~{r_score:.2f}",
        prior_score="N/A",
        equity_ceiling=f"{aras_output.equity_ceiling_pct:.0%}",
        queue_trigger="0.65",
        ares_status="Confirming" if not raw_monitor.ares_status.is_fully_cleared else "Cleared",
        score_drivers=(
            f"VIX {raw_monitor.macro_inputs.get('VIX_INDEX', 'N/A')} · "
            f"HY Spread {raw_monitor.macro_inputs.get('HY_CREDIT_SPREAD', 'N/A')} · "
            f"PMI {raw_monitor.macro_inputs.get('PMI_NOWCAST', 'N/A')} · "
            f"10Y {raw_monitor.macro_inputs.get('10Y_TREASURY_YIELD', 'N/A')} · "
            f"RPE {raw_monitor.rpe.highest_prob_transition} {raw_monitor.rpe.highest_prob_value:.1%}"
        ),
        sp500_futures="N/A",
        nasdaq_futures="N/A",
        brent_crude=(f"${raw_monitor.macro_inputs.get('DCOILBRENTEU'):.2f}" if raw_monitor.macro_inputs.get('DCOILBRENTEU') is not None else "N/A"),
        vix=(f"{raw_monitor.macro_inputs.get('VIX_INDEX'):.2f}" if raw_monitor.macro_inputs.get('VIX_INDEX') is not None else "N/A"),
        treasury_10y=(f"{raw_monitor.macro_inputs.get('10Y_TREASURY_YIELD'):.2f}%" if raw_monitor.macro_inputs.get('10Y_TREASURY_YIELD') is not None else "N/A"),
        equity_book=book_view,
        deployment_queue=queue_view,
        sgol_weight=(f"{raw_monitor.sleeve_weights.get('SGOL', 0.0):.1%}" if 'SGOL' in raw_monitor.sleeve_weights else "N/A"),
        dbmf_weight=(f"{raw_monitor.sleeve_weights.get('DBMF', 0.0):.1%}" if 'DBMF' in raw_monitor.sleeve_weights else "N/A"),
        sgov_weight=(f"{raw_monitor.sleeve_weights.get('SGOV', 0.0):.1%}" if 'SGOV' in raw_monitor.sleeve_weights else "N/A"),
        strc_weight=(f"{raw_monitor.sleeve_weights.get('STRC', 0.0):.1%}" if 'STRC' in raw_monitor.sleeve_weights else "N/A"),
        ptrh_status_str=f"{raw_monitor.ptrh.actual_notional_pct:.2%} NAV",
        cash_weight=f"{cash_hedge:.1%}",
        cash_context=(
            f"Portfolio summary: equity exposure {equity_exposure:.1%}, defensive sleeve {defensive_sleeve:.1%}, cash/hedge {cash_hedge:.1%}, AI-capex sleeve {raw_monitor.portfolio_summary.get('ai_sector_exposure_pct', 0.0):.1%}."
        ),
        modules=modules,
        alerts=alerts,
        decisions=decisions
    )
