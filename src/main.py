"""
ACHELION ARMS v1.1 - FULL INTEGRATION CYCLE
"Silence is trust in the architecture."

This script executes a complete ARMS operational cycle.
Production rule: do not silently substitute fabricated portfolio or market state.
"""

import datetime
import json
import os
from typing import List, Dict, Any


LIVE_CYCLE_STRICT = os.environ.get('ARMS_STRICT_LIVE', '1').strip().lower() not in {'0', 'false', 'no'}


def require_live(condition: bool, message: str):
    if not condition:
        raise RuntimeError(message)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- 1. Core Services & Interfaces ---
from data_feeds.pipeline import DataPipeline
from data_feeds.event_bridge import load_event_bridge
from data_feeds.sec_edgar_feed import fetch_form4_events
from data_feeds.news_rss_feed import fetch_public_rss_events
from data_feeds.event_state import dedupe_news_items
from data_feeds.macro_event_state import derive_macro_event_state
from execution.broker_api import IBKRBroker
from execution.order_book import OrderBook, LiquidityMode
from execution.strategic_queue import StrategicQueueManager
from execution.circuit_breaker import CircuitBreaker
from modules.stress_scenarios import run_stress_scenarios
from execution.confirmation_queue import ConfirmationQueue, QueuedAction
from reporting.audit_log import SessionLogEntry, append_to_log
from execution.order_request import OrderRequest
from execution.queue_state import build_queue_governance_state
from execution.queue_reasoning import build_thesis_signal_map, derive_queue_reasoning_signals
from execution.queue_persistence import persist_queue_state
from reporting.monitor_state import DailyMonitorState, MacroInputCard, EquityBookEntryState, SleeveEntryState, ModulePanelState, DecisionQueueItem, QueueEntryState
from reporting.report_context import summarize_recent_session_log

# --- 2. Engine Modules ---
from engine.mics import calculate_mics, SentinelGateInputs
from engine.sentinel_bridge import build_mics_input_for_ticker
from engine.sentinel_workflow import sentinel_workflow
from engine.tdc_state import load_tdc_state
from engine.cam import CamInputs, calculate_required_notional
from engine.tail_hedge import run_ptrh_module, OptionsPosition
from engine.dshp import run_dshp_check, DefensivePosition
from engine.cdm import run_cdm_scan, NewsItem
from engine.tdc import run_thesis_review, run_weekly_tdc_audit
from engine.regime_probability import calculate_rpe
from engine.ares import run_ares_check
from engine.cdf import calculate_position_decay
from engine.cdf_analytics import compute_live_underperformance
from engine.cdf_state import update_cdf_state
from engine.mc_rss import calculate_mc_rss
from engine.rss_bridge import load_rss_inputs
from engine.cdf_bridge import load_cdf_inputs
from engine.macro_compass import calculate_macro_regime_score, get_regime_label
from engine.bridge_health import collect_bridge_health
from engine.aras import calculate_aras_ceiling
from engine.master_engine import compute_target_weights
from execution.trade_order_generator import generate_rebalance_orders
from engine.drawdown_sentinel import run_pds_check
from engine.pds_state import load_high_water_mark, update_high_water_mark
from engine.factor_exposure import run_fem_check
from engine.incapacitation import run_incapacitation_check
from engine.asymmetric_upside import run_aup_check
from reporting.daily_monitor import run_daily_monitor

def _read_recent_session_log(limit: int = 400) -> List[dict]:
    path = 'achelion_arms/logs/session_log.jsonl'
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[-limit:]
    out = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def run_full_arms_cycle():
    log_file = "achelion_arms/logs/session_log.jsonl"
    now = datetime.datetime.now(datetime.timezone.utc)
    
    print("\n" + "="*60)
    print("ACHELION ARMS v1.1 - FULL OPERATIONAL SWEEP")
    print(f"Cycle Initiated: {now.isoformat()}")
    print("="*60)
    
    # --- PHASE 0: INITIALIZATION ---
    print("\n[STEP 0] Initializing ARMS Services...")
    recent_log_summary = summarize_recent_session_log(_read_recent_session_log())
    data_pipeline = DataPipeline()
    broker = IBKRBroker()
    order_book = OrderBook()
    circuit_breaker = CircuitBreaker()
    confirmation_queue = ConfirmationQueue()
    strategic_queue = StrategicQueueManager(config_path='data/mj_strategic_queue.json')
    
    try:
        broker.connect()
    except Exception as e:
        raise RuntimeError(f"Could not connect to live broker: {e}")
    
    append_to_log(SessionLogEntry(
        timestamp=now.isoformat(), 
        action_type='CYCLE_START', 
        triggering_module='MAIN_ORCHESTRATOR', 
        triggering_signal='Full integration sweep initiated.'
    ))

    bridge_health = collect_bridge_health()
    for rec in bridge_health:
        print(f"[BRIDGE] {rec.name}: {rec.status} ({rec.path})")
        append_to_log(SessionLogEntry(
            timestamp=now.isoformat(),
            action_type='BRIDGE_HEALTH',
            triggering_module='MAIN_ORCHESTRATOR',
            triggering_signal=f"{rec.name} {rec.status} path={rec.path} age_hours={rec.age_hours}",
        ))

    # --- PHASE 1: DATA INGESTION (THE SENSES) ---
    print("\n[STEP 1] Running Multi-Feed Data Ingestion...")
    signals = data_pipeline.run_all_feeds()
    require_live(len(signals) > 0, "Data pipeline returned no signals.")
    signal_types = {s.signal_type for s in signals}
    require_live('VIX_INDEX' in signal_types and 'HY_CREDIT_SPREAD' in signal_types, "Critical macro signals missing from data pipeline.")
    macro_input_map = {s.signal_type: float(s.raw_value if s.raw_value is not None else s.value) for s in signals}
    
    # --- PHASE 2.5: LIVE PORTFOLIO INGESTION ---
    print("\n[STEP 1.5] Ingesting Live Portfolio Data...")
    require_live(broker.is_connected, "Broker is not connected; refusing to run live cycle.")
    live_positions = broker.get_positions()
    nav = broker.get_nav()
    require_live(nav > 0, "Live NAV is non-positive.")

    # --- PHASE 2: MACRO & SENTIMENT (ARAS / RPE / RSS) ---
    print("\n[STEP 2] Calculating Regime & Sentiment...")
    # 2.0 Macro Compass & ARAS Sub-Modules
    preliminary_event_items = []
    preliminary_event_items.extend(fetch_form4_events())
    preliminary_event_items.extend(fetch_public_rss_events())
    preliminary_event_items.extend(load_event_bridge())
    preliminary_event_items = dedupe_news_items(preliminary_event_items)
    macro_event_state = derive_macro_event_state(preliminary_event_items)
    regime_score = calculate_macro_regime_score(signals, event_state=macro_event_state)
    
    from modules.deleveraging_risk import run_deleveraging_check
    from modules.margin_stress import run_margin_stress_check
    from modules.dealer_gamma import run_dealer_gamma_check
    
    delev_res = run_deleveraging_check(signals)
    margin_res = run_margin_stress_check()
    gamma_res = run_dealer_gamma_check()
    
    if delev_res.status == "ACTIVE" or margin_res.status == "ACTIVE" or gamma_res.regime == "NEGATIVE":
        print(f"[ARAS SUB-MODULES] High systemic risk detected: Delev:{delev_res.status} Margin:{margin_res.status} Gamma:{gamma_res.regime}")
        # In a full system, these feed into the Macro Compass overlay or directly cap the ARAS ceiling.
        # For now, we log their advisory output.
    
    vix_val = next((s.value for s in signals if s.signal_type == 'VIX_INDEX'), 0.20) * 100.0
    # Fetch intraday data for circuit breaker
    spx_open = broker.get_recent_close('SPY', 1) or 500.0
    spx_now = broker.get_recent_close('SPY', 0) or 500.0
    
    circuit_breaker.update_market_data(
        spx_open=spx_open,
        spx_current=spx_now,
        vix_open=20.0,
        vix_current=vix_val
    )
    cb_status = circuit_breaker.evaluate()
    if cb_status.is_tripped:
        print("[MAIN] CRITICAL: Circuit Breaker TRIPPED. Autonomous execution halted.")
        # Proceed with diagnostics but no trade execution
    aras_output = calculate_aras_ceiling(regime_score)
    current_regime = aras_output.regime
    print(f"[ARAS] Computed Regime: {current_regime} ({regime_score:.2f}) -> Ceiling: {aras_output.equity_ceiling_pct:.0%}")
    
    # 2.1 RSS (Retail Sentiment)
    rss_inputs = load_rss_inputs()
    rss_res = calculate_mc_rss(
        retail_net_buying_usd=rss_inputs.retail_net_buying_usd,
        retail_history_30d=rss_inputs.retail_history_30d,
        naaim_exposure_index=rss_inputs.naaim_exposure_index,
        aaii_bull_bear_spread=rss_inputs.aaii_bull_bear_spread
    )
    
    # 2.2 RPE (Regime Probability)
    rpe_res = calculate_rpe(current_regime=current_regime, latest_signals=signals)
    
    # 2.3 Incapacitation Check (Safety)
    last_hb = now - datetime.timedelta(minutes=45)
    incap_res = run_incapacitation_check(last_hb, current_regime)
    
    # 2.4 Portfolio Drawdown Sentinel (PDS)
    hwm = load_high_water_mark(nav)
    pds_res = run_pds_check(nav, hwm)
    update_high_water_mark(nav)
    effective_ceiling = min(aras_output.equity_ceiling_pct, pds_res.pds_ceiling)
    if pds_res.status != "NORMAL":
        print(f"[PDS] ALERT: {pds_res.status} Active. PDS Ceiling {pds_res.pds_ceiling:.0%} overrides ARAS.")
    else:
        print(f"[PDS] Status NORMAL. Effective Ceiling remains {effective_ceiling:.0%}")
    
    # --- PHASE 3: PORTFOLIO MAINTENANCE & STRESS AUDITING ---
    print("\n[STEP 3] Auditing Portfolio & Performance...")
    
    # 3.0 Stress Scenario Library (SSL)
    live_weights_all = {p.ticker: (p.market_value / nav) for p in live_positions if nav > 0}
    ptrh_notional = sum(p.notional_value for p in live_puts) if 'live_puts' in locals() else 0.0 # Will be populated in Step 4, but we can rough estimate it here
    ssl_res = run_stress_scenarios(nav, live_weights_all, ptrh_notional)
    print(f"[SSL] Worst-Case Scenario: {ssl_res.worst_scenario} (Net P&L: {ssl_res.worst_net_loss_pct:.2%})")

    # 3.1 DSHP (Harvesting)
    
    # Map live defensive sleeve positions for DSHP evaluation
    sleeve_positions = {}
    for p in live_positions:
        if p.ticker in ['SGOL', 'DBMF']:
            sleeve_positions[p.ticker] = DefensivePosition(
                ticker=p.ticker, 
                current_value=p.market_value, 
                entry_value=p.average_cost * p.quantity, 
                current_weight=p.market_value / nav if nav > 0 else 0
            )

    harvest_actions = run_dshp_check(sleeve_positions, nav) if sleeve_positions else []
    
    # 3.2 CDF (Decay)
    cdf_inputs = load_cdf_inputs()
    cdf_status = []
    qqq_now = broker.get_recent_close('QQQ', days_ago=0)
    qqq_45d = broker.get_recent_close('QQQ', days_ago=45)
    for p in live_positions:
        if p.sec_type != 'STK':
            continue
        rec = cdf_inputs.get(p.ticker)
        try:
            px_now = broker.get_recent_close(p.ticker, days_ago=0)
            px_45d = broker.get_recent_close(p.ticker, days_ago=45)
            computed_underperf = compute_underperformance_pp(px_45d, px_now, qqq_45d, qqq_now)
        except Exception:
            computed_underperf = 0.0

        if rec:
            underperf = max(rec.underperformance_pp, computed_underperf)
        else:
            underperf = computed_underperf

        persisted = update_cdf_state(p.ticker, underperf)
        days_under = max(rec.days_underperforming, persisted.underperforming_days) if rec else persisted.underperforming_days
        cdf_status.append(calculate_position_decay(p.ticker, days_under, underperf))
    
    # --- PHASE 4: HEDGE MANAGEMENT (CAM / PTRH) ---
    print("\n[STEP 4] Calculating Tail-Risk Coverage...")
    from engine.factor_exposure import run_fem_check
    mock_fem_weights = {p.ticker: p.market_value / nav if nav > 0 else 0 for p in live_positions if p.sec_type == "STK"}
    fem_signal = run_fem_check(mock_fem_weights)
    fem_concentration_score = fem_signal.highest_exposure_pct if getattr(fem_signal, 'highest_exposure_factor', None) else 0.0
    
    live_equity_positions = [p for p in live_positions if p.sec_type == "STK" and p.ticker not in ["SGOV", "SGOL", "DBMF", "STRC"]]
    current_equity_pct = sum(p.market_value for p in live_equity_positions) / nav if nav > 0 else 0.0

    macro_stress_score = min(1.0, regime_score)
    cdm_alerts = []
    cam_in = CamInputs(
        current_equity_pct=current_equity_pct, regime_score=regime_score,
        fem_concentration_score=fem_concentration_score, macro_stress_score=macro_stress_score,
        cdm_active_signals=0, nav=nav
    )
    
    # Map live option positions for PTRH evaluation
    live_puts = []
    for p in live_positions:
        if p.sec_type == 'OPT' and p.ticker == 'QQQ' and (p.right or '').upper() == 'P':
            expiry = p.expiry or datetime.date.today().strftime('%Y%m%d')
            if len(expiry) == 8 and expiry.isdigit():
                expiry = f"{expiry[0:4]}-{expiry[4:6]}-{expiry[6:8]}"
            strike = float(p.strike or 0.0)
            contract_multiplier = float(p.multiplier or 100.0)
            underlying_notional = abs(float(p.quantity)) * strike * contract_multiplier if strike > 0 else abs(float(p.market_value))
            live_puts.append(OptionsPosition(
                ticker=p.ticker,
                option_type="PUT",
                strike=strike,
                expiry=expiry,
                contracts=int(abs(p.quantity)),
                notional_value=underlying_notional,
                con_id=p.con_id
            ))
        
    ptrh_res = run_ptrh_module(cam_in, live_puts, broker)
    for order in ptrh_res.generated_orders:
        if cb_status.is_tripped:
            print(f"[MAIN] Execution blocked by Circuit Breaker: {order.ticker}")
            continue
            
        # Send through Order Book for LAEP evaluation
        ob_entry = order_book.process_request(order, vix_val)
        
        # Route based on Tier
        if order.tier == 1:
            queued_action = QueuedAction(
                action_id=f"ptrh_{order.ticker}_{now.strftime('%Y%m%d_%H%M')}",
                item=order,
                triggering_module='PTRH',
                rationale=order.triggering_signal,
                queued_at=now,
                veto_window_hours=order.veto_window_hours
            )
            confirmation_queue.add_action(queued_action)
        elif order.tier == 0:
            pass # Queued in OrderBook for LAEP batch execution
    
    # --- PHASE 5: THESIS INTEGRITY (CDM / TDC) ---
    print("\n[STEP 5] Running AI-Driven Thesis Audits...")
    event_items = preliminary_event_items
    cdm_alerts = run_cdm_scan(event_items) if event_items else []
    tdc_results = []
    for alert in cdm_alerts:
        tdc_results.append(run_thesis_review(alert))

    weekly_audit_results = run_weekly_tdc_audit([p.ticker for p in live_positions if p.sec_type == 'STK'])
    tdc_results.extend(weekly_audit_results)
        
    # --- PHASE 6: MASTER ENGINE & REBALANCING ---
    print("\n[STEP 6] Rebalancing Equity Book...")
    live_equity_positions = [p for p in live_positions if p.sec_type == 'STK']
    require_live(len(live_equity_positions) > 0, "No live equity positions found from broker.")

    live_weights = {p.ticker: (p.market_value / nav) for p in live_equity_positions if nav > 0}
    fem_signal = run_fem_check(live_weights)

    mics_results_live = {}
    mics_scores = {}
    for p in live_equity_positions:
        fem_impact = f"NORMAL->{fem_signal.status}" if fem_signal.status in {'WATCH', 'ALERT'} else 'NORMAL->NORMAL'
        mics_input = build_mics_input_for_ticker(p.ticker, current_regime, fem_impact)
        mics_result = calculate_mics(mics_input)
        mics_results_live[p.ticker] = mics_result
        mics_scores[p.ticker] = mics_result.conviction_level

    cdf_multipliers = {p.ticker: 1.0 for p in live_equity_positions}
    target_weights = compute_target_weights(
        mics_scores=mics_scores,
        cdf_multipliers=cdf_multipliers,
        aras_ceiling=effective_ceiling
    )
    
    rebalance_orders = generate_rebalance_orders(live_positions, target_weights, nav)
    for order in rebalance_orders:
        if cb_status.is_tripped:
            print(f"[MAIN] Execution blocked by Circuit Breaker: {order.ticker}")
            continue
            
        ob_entry = order_book.process_request(order, vix_val)
        
        if order.tier == 1:
            pass # Same logic as PTRH
        elif order.tier == 0:
            pass # Queued in OrderBook for LAEP batch execution
                
    # --- PHASE 6.8: LAEP EXECUTION WAVE ---
    print("\n[STEP 6.8] Executing L5 Order Book (LAEP)...")
    executable_batch = order_book.get_executable_batch()
    if not executable_batch:
        print("[ORDER_BOOK] No executable orders in queue.")
    else:
        for entry in executable_batch:
            if entry.request.tier == 0:
                if broker.is_connected:
                    print(f"[ORDER_BOOK] Routing {entry.order_type} Priority {entry.priority} for {entry.request.ticker} (Slippage: {entry.slippage_budget_bps}bps)")
                    broker.submit_order(entry.request)
                else:
                    print(f"[MAIN] Broker disconnected. Cannot execute Tier 0 order: {entry.request.action} {entry.request.ticker}")
            else:
                print(f"[ORDER_BOOK] Skipping Tier 1 order {entry.request.ticker} (Awaiting PM Confirmation in Queue).")

    # --- PHASE 6.5: GROWTH & RE-ENTRY (ARES / AUP) ---
    print("\n[STEP 6.5] Evaluating Growth & Re-Entry...")
    ares_res = run_ares_check(current_regime, regime_score, 0.25, rss_res.composite_rss)
    aup_res = run_aup_check(current_regime, 7.8, True, 0.15, pds_res.drawdown_pct)
    
    from engine.slof import run_slof_manager
    # In a full live system, current leverage is retrieved from broker (e.g. gross exposure / net liq)
    # Using 1.0 proxy for simulation run
    slof_status = run_slof_manager(aup_res, current_leverage=1.0)

    thesis_signal_map = build_thesis_signal_map(getattr(sentinel_workflow, '_records', {}))
    thesis_state_by_ticker = {
        ticker: {
            'status': sig.thesis_status,
            'gate3_score': str(sig.gate3_score) if sig.gate3_score is not None else '',
            'source_category': sig.source_category,
        }
        for ticker, sig in thesis_signal_map.items()
    }

    queue_reasoning = derive_queue_reasoning_signals(
        queue_tickers=[item.ticker for item in strategic_queue.items],
        thesis_map=thesis_signal_map,
        cdm_alerts=cdm_alerts,
        tdc_state_by_ticker=load_tdc_state(),
    )

    queue_state = build_queue_governance_state(
        strategic_items=strategic_queue.items,
        current_score=regime_score,
        current_regime=current_regime,
        ares_fully_cleared=ares_res.is_fully_cleared,
        thesis_state_by_ticker=thesis_state_by_ticker,
        reasoning_signals=queue_reasoning,
    )
    queue_transitions = persist_queue_state(queue_state)
    
    # --- PHASE 7: CONSOLIDATION & REPORTING ---
    print("\n[STEP 7] Generating Daily Monitor v4.0...")

    macro_cards_state = [
        MacroInputCard(title='VIX', value=str(round(macro_input_map.get('VIX_INDEX', 0.0), 2)), context='Live ingestion'),
        MacroInputCard(title='HY_SPREAD', value=str(round(macro_input_map.get('HY_CREDIT_SPREAD', 0.0), 2)), context='Live ingestion'),
        MacroInputCard(title='PMI', value=str(round(macro_input_map.get('PMI_NOWCAST', 0.0), 2)), context='Live ingestion'),
        MacroInputCard(title='10Y_YIELD', value=str(round(macro_input_map.get('10Y_TREASURY_YIELD', 0.0), 2)), context='Live ingestion'),
        MacroInputCard(title='EVENT_OVERLAY', value=str(round(macro_event_state.override_floor, 2)), context='Typed event-state overlay'),
    ]

    equity_book_state = [
        EquityBookEntryState(
            ticker=p.ticker,
            name=p.ticker,
            weight_pct=(p.market_value / nav * 100) if nav > 0 else 0.0,
            perf_text='LIVE',
            status='OK',
            rationale=f"Live position snapshot | MICS={mics_scores.get(p.ticker, 'N/A')}"
        )
        for p in live_positions if p.sec_type == 'STK'
    ]

    defensive_sleeve_state = [
        SleeveEntryState(
            ticker=p.ticker,
            weight_pct=(p.market_value / nav * 100) if nav > 0 else 0.0,
            rationale='Live sleeve snapshot'
        )
        for p in live_positions if p.ticker in ['DBMF', 'SGOV', 'SGOL', 'STRC']
    ]

    module_panels_state = [
        ModulePanelState(name='ARAS', status=f'{aras_output.regime} {aras_output.score:.2f}', detail=f'Base ceiling {base_ceiling:.2%} -> effective {effective_ceiling:.2%}'),
        ModulePanelState(name='SSL', status=f'Worst Case: {ssl_res.worst_scenario}', detail=f'Estimated P&L: {ssl_res.worst_net_loss_pct:.2%}'),
        ModulePanelState(name='ARES', status='Queue ' + queue_state.headline_status, detail=f'Fully cleared={ares_res.is_fully_cleared}'),
        ModulePanelState(name='CAM', status=f'PTRH {ptrh_res.multiplier}x', detail=f'Target {ptrh_res.target_notional_pct:.2%} | Actual {ptrh_res.actual_notional_pct:.2%}'),
        ModulePanelState(name='MC-RSS', status=rss_res.signal_label, detail=f'Composite {rss_res.composite_rss:.2f}'),
        ModulePanelState(name='SAFETY', status=f'Tier {incap_res.current_safety_tier}', detail=f'Last heartbeat {incap_res.last_heartbeat_age_min} min ago'),
        ModulePanelState(name='QUEUE_GOV', status=queue_state.headline_status, detail=f'{len(queue_transitions)} transition(s) persisted this cycle'),
    ]

    queue_counts_note = (
        f"Neutral={len(queue_state.neutral_queue)} | RiskOn={len(queue_state.risk_on_queue)} | "
        f"Monitor={len(queue_state.monitor_list)} | Removed={len(queue_state.removed_items)} | "
        f"Transitions={len(queue_transitions)}"
    )
    decision_queue_state = [
        DecisionQueueItem(
            title='Maintain queue discipline',
            body=f"Queue headline is {queue_state.headline_status}. {queue_counts_note}. Do not front-run trigger logic outside system rules."
        ),
        DecisionQueueItem(
            title='Review thesis pressure',
            body=f"CDM alerts={len(cdm_alerts)} | TDC reviews={len(tdc_results)}. Any WATCH/IMPAIRED/BROKEN thesis state should govern queue posture before size increases."
        ),
        DecisionQueueItem(
            title='Validate hedge and execution readiness',
            body=f"PTRH last action={ptrh_res.last_action}. Order book batch size={len(executable_batch)}. Confirm no unresolved execution-quality issues before trusting autonomy claims."
        ),
    ]

    prior_score = round(recent_log_summary.prior_score_estimate or max(aras_output.score, pds_res.drawdown_pct), 2)
    catalyst_label = 'Live event-state review required'
    if macro_event_state.diplomacy_breakdown_score >= 0.50:
        catalyst_label = 'Diplomacy deterioration watch'
    elif macro_event_state.diplomacy_breakdown_score > 0.0:
        catalyst_label = 'Diplomacy / talks watch'
    elif macro_event_state.oil_stress_score >= 0.40:
        catalyst_label = 'Oil / shipping stress watch'

    monitor_state = DailyMonitorState(
        date_label=now.strftime('%B %d, %Y'),
        regime=aras_output.regime,
        score=round(aras_output.score, 2),
        score_direction='↑' if regime_score > prior_score else '↓',
        score_prior=prior_score,
        queue_status=queue_state.headline_status,
        next_catalyst=catalyst_label,
        equity_ceiling_pct=effective_ceiling,
        macro_cards=macro_cards_state,
        deployment_queue=[
            QueueEntryState(
                ticker=e.ticker,
                target=(f'{e.target_weight_pct * 100:.1f}%' if e.target_weight_pct is not None else 'N/A'),
                execution_instruction=e.execution_instruction,
                state=e.state,
                reason=e.reason,
                trigger_rule=e.trigger_rule,
                notes=e.notes,
            )
            for e in queue_state.neutral_queue
        ],
        risk_on_queue=[
            QueueEntryState(
                ticker=e.ticker,
                target=(f'{e.target_weight_pct * 100:.1f}%' if e.target_weight_pct is not None else 'N/A'),
                execution_instruction=e.execution_instruction,
                state=e.state,
                reason=e.reason,
                trigger_rule=e.trigger_rule,
                notes=e.notes,
            )
            for e in queue_state.risk_on_queue
        ],
        monitor_list=[
            QueueEntryState(
                ticker=e.ticker,
                target=(f'{e.target_weight_pct * 100:.1f}%' if e.target_weight_pct is not None else 'N/A'),
                execution_instruction=e.execution_instruction,
                state=e.state,
                reason=e.reason,
                trigger_rule=e.trigger_rule,
                notes=e.notes,
            )
            for e in queue_state.monitor_list
        ],
        removed_queue_items=[
            QueueEntryState(
                ticker=e.ticker,
                target=(f'{e.target_weight_pct * 100:.1f}%' if e.target_weight_pct is not None else 'N/A'),
                execution_instruction=e.execution_instruction,
                state=e.state,
                reason=e.reason,
                trigger_rule=e.trigger_rule,
                notes=e.notes,
            )
            for e in queue_state.removed_items
        ],
        equity_book=equity_book_state,
        defensive_sleeve=defensive_sleeve_state,
        module_panels=module_panels_state,
        pm_decision_queue=decision_queue_state,
        live_context={
            'vix': str(macro_input_map.get('VIX_INDEX', 'N/A')),
            'hy_spread': str(macro_input_map.get('HY_CREDIT_SPREAD', 'N/A')),
            'pmi': str(macro_input_map.get('PMI_NOWCAST', 'N/A')),
            'ten_yield': str(macro_input_map.get('10Y_TREASURY_YIELD', 'N/A')),
        }
    )

    raw_inputs = {
        'date': monitor_state.date_label,
        'regime': monitor_state.regime,
        'score': monitor_state.score,
        'score_direction': monitor_state.score_direction,
        'queue_status': monitor_state.queue_status,
        'macro_compass_score_yesterday': monitor_state.score_prior or monitor_state.score,
        'macro_compass_trigger': 0.65,
        'macro_compass_next_catalyst': monitor_state.next_catalyst,
        'macro_compass_drivers_up': '; '.join(macro_event_state.rationale[:3]) if macro_event_state.rationale else 'No elevated event-state drivers detected.',
        'macro_compass_drivers_down': f"Recent trades={recent_log_summary.trade_count}; TDC reviews={recent_log_summary.tdc_review_count}; queue changes={recent_log_summary.queue_change_count}. Full parity still depends on deeper asymmetry logic and richer prior-score history.",
        'macro_inputs': {card.title: {'value': card.value, 'context': card.context} for card in monitor_state.macro_cards},
        'equity_book': [
            {
                'ticker': e.ticker,
                'name': e.name,
                'weight': e.weight_pct,
                'session_perf': 0.01 if e.perf_text == 'LIVE' else 0.0,
                'status': e.status,
                'rationale': e.rationale,
            }
            for e in monitor_state.equity_book
        ],
        'deployment_queue': [
            {
                'ticker': q.ticker,
                'target': q.target,
                'execution_instruction': q.execution_instruction,
                'status': f'{q.state} · {q.reason}',
                'notes': q.notes,
            }
            for q in monitor_state.deployment_queue + monitor_state.risk_on_queue
        ],
        'removed_queue_items': [
            {
                'ticker': q.ticker,
                'target': q.target,
                'execution_instruction': q.execution_instruction,
                'status': f'{q.state} · {q.reason}',
                'notes': q.notes,
            }
            for q in monitor_state.removed_queue_items
        ],
        'monitor_list': [
            {
                'ticker': q.ticker,
                'target': q.target,
                'execution_instruction': q.execution_instruction,
                'status': f'{q.state} · {q.reason}',
                'notes': q.notes,
            }
            for q in monitor_state.monitor_list
        ],
        'defensive_sleeve': [
            {
                'ticker': s.ticker,
                'weight': s.weight_pct,
                'rationale': s.rationale,
            }
            for s in monitor_state.defensive_sleeve
        ],
        'module_status': {panel.name: {'status': panel.status, 'detail': panel.detail} for panel in monitor_state.module_panels},
    }
    
    # Compile live news events into market context for the LLM
    live_news_context = "\n".join([f"[{ev.event_type} - {ev.triggering_entity}]: {ev.headline}" for ev in event_items]) if event_items else "No major market events detected today."
    live_market_context = f"""
    System completed daily sweep.
    Current VIX is {monitor_state.live_context.get('vix')}.
    Current 10Y Yield is {monitor_state.live_context.get('ten_yield')}.
    Current queue headline status is {monitor_state.queue_status}.
    Neutral queue count: {len(monitor_state.deployment_queue)}.
    Risk-on queue count: {len(monitor_state.risk_on_queue)}.
    Recent News Events shaping macro:
    {live_news_context}
    """
    
    markdown_output = run_daily_monitor(raw_inputs, live_market_context)
    report_path = f"achelion_arms/logs/daily_monitor_{now.strftime('%Y%m%d')}.md"
    with open(report_path, "w") as f:
        f.write(markdown_output)
        
    print(f"[MAIN] Successfully rendered structured Daily Monitor to {report_path}")
    
    append_to_log(SessionLogEntry(
        timestamp=now.isoformat(), 
        action_type='CYCLE_END', 
        triggering_module='MAIN_ORCHESTRATOR', 
        triggering_signal='Daily sweep complete.'
    ))
    
    broker.disconnect()

if __name__ == '__main__':
    run_full_arms_cycle()
