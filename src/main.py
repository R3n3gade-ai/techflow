"""
ACHELION ARMS v1.1 - FULL INTEGRATION CYCLE
"Silence is trust in the architecture."

This script executes a complete ARMS operational cycle, integrating all 
Phase 1, 2, and 3 modules. It simulates the 6:00 AM CT sweep.
"""

import datetime
import json
import os
from typing import List, Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- 1. Core Services & Interfaces ---
from data_feeds.pipeline import DataPipeline
from execution.broker_api import IBKRBroker
from execution.order_book import OrderBook, LiquidityMode
from execution.circuit_breaker import CircuitBreaker
from modules.stress_scenarios import run_stress_scenarios
from execution.confirmation_queue import ConfirmationQueue, QueuedAction
from reporting.audit_log import SessionLogEntry, append_to_log
from execution.order_request import OrderRequest

# --- 2. Engine Modules ---
from engine.mics import calculate_mics, SentinelGateInputs
from engine.cam import CamInputs, calculate_required_notional
from engine.tail_hedge import run_ptrh_module, OptionsPosition
from engine.dshp import run_dshp_check, DefensivePosition
from engine.cdm import run_cdm_scan, NewsItem
from engine.tdc import run_thesis_review
from engine.regime_probability import calculate_rpe
from engine.ares import run_ares_check
from engine.cdf import calculate_position_decay
from engine.mc_rss import calculate_mc_rss
from engine.macro_compass import calculate_macro_regime_score, get_regime_label
from engine.aras import calculate_aras_ceiling
from engine.master_engine import compute_target_weights
from execution.trade_order_generator import generate_rebalance_orders
from engine.drawdown_sentinel import run_pds_check
from engine.factor_exposure import run_fem_check
from engine.incapacitation import run_incapacitation_check
from engine.asymmetric_upside import run_aup_check
from reporting.daily_monitor import generate_daily_monitor
from reporting.daily_monitor_view import build_view_model
from reporting.daily_monitor_renderer import render_html_report

def run_full_arms_cycle():
    log_file = "achelion_arms/logs/session_log.jsonl"
    now = datetime.datetime.now(datetime.timezone.utc)
    
    print("\n" + "="*60)
    print("ACHELION ARMS v1.1 - FULL OPERATIONAL SWEEP")
    print(f"Cycle Initiated: {now.isoformat()}")
    print("="*60)
    
    # --- PHASE 0: INITIALIZATION ---
    print("\n[STEP 0] Initializing ARMS Services...")
    data_pipeline = DataPipeline()
    broker = IBKRBroker()
    order_book = OrderBook()
    circuit_breaker = CircuitBreaker()
    confirmation_queue = ConfirmationQueue()
    
    try:
        broker.connect()
    except Exception as e:
        print(f"[MAIN] WARNING: Could not connect to live broker ({e}). Continuing in decoupled mode.")
    
    append_to_log(SessionLogEntry(
        timestamp=now.isoformat(), 
        action_type='CYCLE_START', 
        triggering_module='MAIN_ORCHESTRATOR', 
        triggering_signal='Full integration sweep initiated.'
    ))

    # --- PHASE 1: DATA INGESTION (THE SENSES) ---
    print("\n[STEP 1] Running Multi-Feed Data Ingestion...")
    signals = data_pipeline.run_all_feeds()
    # Extract specific values for downstream engines
    # (Simulating extraction from SignalRecord list)
    vix_val = 14.5
    sp_pmi = 0.515
    btc_funding = 0.0001
    
    # --- PHASE 2.5: LIVE PORTFOLIO INGESTION ---
    print("\n[STEP 1.5] Ingesting Live Portfolio Data...")
    if broker.is_connected:
        try:
            live_positions = broker.get_positions()
            nav = broker.get_nav()
        except Exception as e:
            print(f"[MAIN] WARNING: Failed to fetch live portfolio ({e}). Using fallback.")
            live_positions = []
            nav = 50_000_000.0
    else:
        live_positions = []
        nav = 50_000_000.0

    # --- PHASE 2: MACRO & SENTIMENT (ARAS / RPE / RSS) ---
    print("\n[STEP 2] Calculating Regime & Sentiment...")
    # 2.0 Macro Compass & ARAS
    regime_score = calculate_macro_regime_score(signals)
    
    vix_val = next((s.value for s in signals if s.signal_type == 'VIX_INDEX'), 0.20) * 100.0
    cb_status = circuit_breaker.evaluate() # Normally uses live intraday change, mock check here
    if cb_status.is_tripped:
        print("[MAIN] CRITICAL: Circuit Breaker TRIPPED. Autonomous execution halted.")
        # Proceed with diagnostics but no trade execution
    aras_output = calculate_aras_ceiling(regime_score)
    current_regime = aras_output.regime
    print(f"[ARAS] Computed Regime: {current_regime} ({regime_score:.2f}) -> Ceiling: {aras_output.equity_ceiling_pct:.0%}")
    
    # 2.1 RSS (Retail Sentiment)
    rss_res = calculate_mc_rss(
        retail_net_buying_usd=1.2e9, 
        retail_history_30d=[1.1e9, 1.3e9], 
        naaim_exposure_index=85.0, 
        aaii_bull_bear_spread=0.20
    )
    
    # 2.2 RPE (Regime Probability)
    rpe_res = calculate_rpe(current_regime=current_regime, latest_signals=signals)
    
    # 2.3 Incapacitation Check (Safety)
    last_hb = now - datetime.timedelta(minutes=45)
    incap_res = run_incapacitation_check(last_hb, current_regime)
    
    # 2.4 Portfolio Drawdown Sentinel (PDS)
    # Using 1.15M as HWM against live NAV for demo
    hwm = 1_150_000.0
    pds_res = run_pds_check(nav, hwm)
    effective_ceiling = min(aras_output.equity_ceiling_pct, pds_res.pds_ceiling)
    if pds_res.status != "NORMAL":
        print(f"[PDS] ALERT: {pds_res.status} Active. PDS Ceiling {pds_res.pds_ceiling:.0%} overrides ARAS.")
    else:
        print(f"[PDS] Status NORMAL. Effective Ceiling remains {effective_ceiling:.0%}")
    
    # --- PHASE 3: PORTFOLIO MAINTENANCE (CDF / DSHP) ---
    print("\n[STEP 3] Auditing Portfolio & Performance...")
    # 3.1 DSHP (Harvesting)
    
    # Map live defensive sleeve positions for DSHP evaluation
    # Assuming SGOL/DBMF might be in the live portfolio. If empty, fall back to mock for demo.
    sleeve_positions = {}
    for p in live_positions:
        if p.ticker in ['SGOL', 'DBMF']:
            sleeve_positions[p.ticker] = DefensivePosition(
                ticker=p.ticker, 
                current_value=p.market_value, 
                entry_value=p.average_cost * p.quantity, 
                current_weight=p.market_value / nav if nav > 0 else 0
            )

    if not sleeve_positions:
        print("[MAIN] No live defensive sleeve detected. Falling back to mock sleeve for DSHP demo.")
        sleeve_positions = {
            'SGOL': DefensivePosition('SGOL', nav * 0.025, nav * 0.02, 0.025) # 25% app
        }
        
    harvest_actions = run_dshp_check(sleeve_positions, nav)
    
    # 3.2 CDF (Decay)
    cdf_status = [calculate_position_decay("TSLA", 10, 2.0)] # Normal
    
    # --- PHASE 4: HEDGE MANAGEMENT (CAM / PTRH) ---
    print("\n[STEP 4] Calculating Tail-Risk Coverage...")
    cam_in = CamInputs(
        current_equity_pct=effective_ceiling, regime_score=regime_score, 
        fem_concentration_score=0.45, macro_stress_score=0.25, 
        cdm_active_signals=0, nav=nav
    )
    
    # Map live option positions for PTRH evaluation
    live_puts = []
    for p in live_positions:
        if p.sec_type == 'OPT' and 'QQQ' in p.ticker:
            # We would normally decode the option ticker string to extract strike/expiry here.
            # For scaffold, we assume any QQQ option is our PTRH.
            live_puts.append(OptionsPosition(p.ticker, "PUT", 0.0, "2026-05-15", int(p.quantity), p.market_value))
    
    if not live_puts:
        print("[MAIN] No live options detected. Falling back to mock QQQ put for PTRH demo.")
        live_puts = [OptionsPosition("QQQ", "PUT", 480, "2026-05-15", 100, 600_000)]
        
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
            if broker.is_connected:
                broker.submit_order(order)
            else:
                print(f"[MAIN] Broker disconnected. Cannot execute Tier 0 order: {order.action} {order.ticker}")
    
    # --- PHASE 5: THESIS INTEGRITY (CDM / TDC) ---
    print("\n[STEP 5] Running AI-Driven Thesis Audits...")
    mock_news = [NewsItem(
        'SEC_EDGAR', 'Alphabet CEO Files Form 4', 'Insider selling detected...', 
        now.isoformat(), ['Alphabet'], 'INSIDER_SALE'
    )]
    cdm_alerts = run_cdm_scan(mock_news)
    tdc_results = []
    for alert in cdm_alerts:
        tdc_results.append(run_thesis_review(alert))
        
    # --- PHASE 6: MASTER ENGINE & REBALANCING ---
    print("\n[STEP 6] Rebalancing Equity Book...")
    target_weights = compute_target_weights(
        mics_scores={'NVDA': 8, 'TSLA': 9, 'MU': 6}, 
        cdf_multipliers={'TSLA': 1.0, 'MU': 0.8}, 
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
            if broker.is_connected:
                broker.submit_order(order)
            else:
                print(f"[MAIN] Broker disconnected. Cannot execute Tier 0 order: {order.action} {order.ticker}")
                
    # --- PHASE 6.5: GROWTH & RE-ENTRY (ARES / AUP) ---
    print("\n[STEP 6.5] Evaluating Growth & Re-Entry...")
    ares_res = run_ares_check(current_regime, regime_score, 0.25, rss_res.composite_rss)
    aup_res = run_aup_check(current_regime, 7.8, True, 0.15, pds_res.drawdown_pct)
    
    # --- PHASE 7: CONSOLIDATION & REPORTING ---
    print("\n[STEP 7] Generating Daily Monitor v2.1...")
    # Mock some data for the monitor aggregator
    mics_results = {"NVDA": calculate_mics(SentinelGateInputs(24, 'Cat B', 'NORMAL', 'WATCH'))}
    
    # Actually add harvest actions to confirmation queue for simulation
    for ha in harvest_actions:
        confirmation_queue.add_action(ha)
        
    monitor = generate_daily_monitor(
        current_regime=current_regime, regime_score=regime_score, rpe_signal=rpe_res,
        ptrh_status=ptrh_res, mics_results=mics_results,
        tdc_results=tdc_results, cdm_alerts=[a.__dict__ for a in cdm_alerts],
        dshp_actions=[ha.to_dict() for ha in harvest_actions], # Simplified for mock
        ares_status=ares_res, cdf_statuses=cdf_status,
        rss_result=rss_res, safety_status=incap_res, nav=nav
    )
    
    print("\n" + "="*60)
    print("SWEEP COMPLETE: MONITOR PAYLOAD READY")
    print(f"Decision Queue Size: {len(monitor.decision_queue)}")
    print(f"Current Regime: {monitor.regime} (Score: {monitor.regime_score})")
    print(f"Anticipatory Signal: {monitor.rpe.highest_prob_transition} ({monitor.rpe.highest_prob_value:.1%})")
    print("="*60)
    
    # --- PHASE 8: REPORT GENERATION ---
    print("\n[STEP 8] Rendering Institutional PDF-Style Briefing...")
    view_model = build_view_model(monitor)
    html_report = render_html_report(view_model)
    
    report_path = f"achelion_arms/logs/daily_monitor_{now.strftime('%Y%m%d')}.html"
    with open(report_path, "w") as f:
        f.write(html_report)
        
    print(f"[MAIN] Successfully rendered structured Daily Monitor to {report_path}")
    
    append_to_log(SessionLogEntry(
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), 
        action_type='CYCLE_END', 
        triggering_module='MAIN_ORCHESTRATOR', 
        triggering_signal='Daily sweep complete.'
    ))
    
    broker.disconnect()

if __name__ == '__main__':
    run_full_arms_cycle()
